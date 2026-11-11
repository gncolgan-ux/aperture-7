import http.server, socketserver, json, time, subprocess, os, hashlib

PORT = 8080
LEDGER_FILE = "aura_live_ledger.json"

if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, 'w') as f: json.dump([], f)

class ApertureDataVault(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
        data_to_store = payload.get("data", "EMPTY")
        
        print(f"\n[+] INBOUND DATA: {str(data_to_store)[:50]}...")
        
        # THE REAL MATH: Feeding an .hx wave into the bare-metal kernel
        hx_wave = f"Set({len(str(data_to_store))}) Shift(2) Math($REG * 1.61803) Echo($REG)"
        try:
            start_calc = time.time()
            result = subprocess.run(
                ["python3", "aperture_kernel.py", hx_wave], 
                capture_output=True, text=True, check=True
            )
            calc_time = (time.time() - start_calc) * 1000
            
            # Extracting the physical kernel output to secure the block
            math_proof = hashlib.sha256(result.stdout.encode()).hexdigest()
            print(f"    -> Kernel Executed in {calc_time:.2f}ms | Proof: {math_proof[:16]}")
        except Exception as e:
            print(f"    -> Kernel Failure: {e}")
            self.send_response(500)
            self.end_headers()
            return

        # VAULTING THE DATA
        with open(LEDGER_FILE, 'r') as f: chain = json.load(f)
        
        new_block = {
            "index": len(chain) + 1,
            "timestamp": time.time(),
            "data": data_to_store,
            "spatial_proof": math_proof
        }
        chain.append(new_block)
        
        with open(LEDGER_FILE, 'w') as f: json.dump(chain, f, indent=2)
        print(f"[+] BLOCK {new_block['index']} VAULTED.")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Vaulted", "block": new_block['index']}).encode())

with socketserver.TCPServer(("", PORT), ApertureDataVault) as httpd:
    print(f"[APERTURE-7] Bare-metal node active. Listening on port {PORT}...")
    httpd.serve_forever()
