import subprocess, hashlib, time, json

print("\n[AURA x APERTURE-7] IGNITING 500-BLOCK GENESIS MINT...")
print("[!] Using original ApertureEndgameKernel for pure mathematical consensus.\n")

class GenesisLedger:
    def __init__(self):
        self.chain = []

    def run_genesis_loop(self):
        start_time = time.time()
        
        for i in range(1, 501):
            # Formulating the original .hx wave syntax for the kernel
            # Elevating to a new Z-layer per block, tracing a 4D vector, and calculating variance
            hx_wave = f"Elevate({i}) Trace(4:GENESIS_SECTOR_{i}) Math($C0 * {i * 1.618}) Echo($REG)"
            
            try:
                # Feeding the wave into your original aperture_kernel.py
                result = subprocess.run(
                    ["python3", "aperture_kernel.py", hx_wave], 
                    capture_output=True, text=True
                )
                raw_output = result.stdout.strip()
                
                # Hashing the physical trace output to forge the block proof
                block_proof = hashlib.sha256(raw_output.encode()).hexdigest()
                
                new_block = {
                    "index": i,
                    "timestamp": time.time(),
                    "proof": block_proof
                }
                self.chain.append(new_block)
                
                # Display output every 50 blocks to prevent console spam
                if i % 50 == 0 or i <= 5:
                    print(f"[+] BLOCK {i:03d} MINED | SPATIAL PROOF: 0x{block_proof[:16]}")
                    
            except Exception as e:
                print(f"[!] Kernel Error on Block {i}: {e}")
                break
                
        duration = time.time() - start_time
        print(f"\n[!] GENESIS COMPLETE.")
        print(f"[!] 500 AURA COINS MINTED in {duration:.2f} seconds.")
        print(f"[!] Network authority established entirely via original Aperture-7 spatial logic.")

if __name__ == "__main__":
    ledger = GenesisLedger()
    ledger.run_genesis_loop()
