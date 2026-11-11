import http.server, socketserver, json, time, subprocess, os, hashlib

PORT = 8080
LEDGER_FILE = os.path.expanduser("~/aperture_workspace/aura_live_ledger.json")
WORKSPACE = os.path.expanduser("~/aperture_workspace")

# The wallet where your compute rewards will accumulate
GENESIS_WALLET = "0xgncolgan_aperture_master"

if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, 'w') as f: json.dump({"chain": [], "wallet_balances": {GENESIS_WALLET: 0}}, f)

class ApertureDataVault(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
        data_to_store = payload.get("data", "EMPTY")
        
        print(f"\n[+] INBOUND DATA: {str(data_to_store)[:50]}...")
        
        # THE REAL MATH: Using absolute paths so the background daemon finds your kernel
        kernel_path = os.path.expanduser("~/Aperture_7/aperture_kernel.py")
        if not os.path.exists(kernel_path):
            kernel_path = os.path.join(WORKSPACE, "aperture_kernel.py")
            
        hx_wave = f"Set({len(str(data_to_store))}) Shift(2) Math($REG * 1.61803) Echo($REG)"
        
        try:
            start_calc = time.time()
            result = subprocess.run(
                ["python3", kernel_path, hx_wave], 
                capture_output=True, text=True, check=True, cwd=WORKSPACE
            )
            calc_time = (time.time() - start_calc) * 1000
            math_proof = hashlib.sha256(result.stdout.encode()).hexdigest()
            print(f"    -> Kernel Executed in {calc_time:.2f}ms | Proof: {math_proof[:16]}")
        except Exception as e:
            print(f"    -> Kernel Failure: Ensure aperture_kernel.py is in {WORKSPACE}")
            self.send_response(500)
            self.end_headers()
            return

        # VAULTING DATA & MINTING BLOCK REWARD
        with open(LEDGER_FILE, 'r') as f: state = json.load(f)
        
        new_block = {
            "index": len(state["chain"]) + 1,
            "timestamp": time.time(),
            "data": data_to_store,
            "spatial_proof": math_proof,
            "miner": GENESIS_WALLET,
            "reward": 1000
        }
        
        state["chain"].append(new_block)
        state["wallet_balances"][GENESIS_WALLET] += 1000
        
        with open(LEDGER_FILE, 'w') as f: json.dump(state, f, indent=2)
        
        print(f"[+] BLOCK {new_block['index']} VAULTED.")
        print(f"[+] MINTED 1,000 AURA to {GENESIS_WALLET}. New Balance: {state['wallet_balances'][GENESIS_WALLET]}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Vaulted", "block": new_block['index'], "reward_issued": 1000}).encode())

with socketserver.TCPServer(("", PORT), ApertureDataVault) as httpd:
    print(f"[APERTURE-7] Minting Node active. Listening on port {PORT}...")
    httpd.serve_forever()
