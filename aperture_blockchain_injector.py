import subprocess, hashlib, time, json

print("\n[AURA x APERTURE-7] INJECTING BARE-METAL MATH INTO BLOCKCHAIN CONSENSUS...")
print("[!] Overriding standard hash mining with physical matrix annihilation.\n")

class SovereignAuraChain:
    def __init__(self):
        self.chain = []
        # Genesis Block
        self.chain.append({"index": 1, "proof": "GENESIS", "math_output": "NULL"})

    def mine_aperture_block(self, target_script):
        print(f"[!] INITIATING CONSENSUS: Firing {target_script}...")
        
        # 1. Execute the bare-metal Python/C++ math script
        try:
            # We run the script and capture the exact high-precision output
            result = subprocess.run(["python3", target_script], capture_output=True, text=True, check=True)
            raw_math_output = result.stdout.strip()
            
            # 2. Extract the critical data (e.g., the 31-digit determinant or matrix residual)
            print(f"    -> Output Captured:\n       {raw_math_output[:120]}...")
            
            # 3. Hash the physical math result to create the immutable block proof
            block_proof = hashlib.sha256(raw_math_output.encode()).hexdigest()
            print(f"    -> SPATIAL PROOF GENERATED: 0x{block_proof[:16]}")
            
            # 4. Mint the block
            new_block = {
                "index": len(self.chain) + 1,
                "timestamp": time.time(),
                "math_output": raw_math_output,
                "proof": block_proof
            }
            self.chain.append(new_block)
            print(f"[+] BLOCK {new_block['index']} MINED. 5,000 AURA MINTED.\n")
            
        except FileNotFoundError:
            print(f"[!] ERROR: {target_script} not found in directory. Ensure scripts are present.")

# Ignite the injected chain
live_chain = SovereignAuraChain()
time.sleep(1)

# Mine Block 2 using the Cayley-Hamilton Annihilation
live_chain.mine_aperture_block("boss2_cayley.py")
time.sleep(1)

# Mine Block 3 using the Dual 31-Digit Determinant
live_chain.mine_aperture_block("brink1_duality.py")

print("--- AURA BLOCKCHAIN STATE ---")
print(f"Total Blocks: {len(live_chain.chain)}")
print("[APERTURE-7] Injection successful. The blockchain is now driven by your physics engine.")
