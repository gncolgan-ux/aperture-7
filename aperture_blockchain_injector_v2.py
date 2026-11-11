import subprocess, hashlib, time, json, os

print("\n[AURA x APERTURE-7] INITIATING SCIENTIFIC CONSENSUS ENGINE...")
print("[!] Harnessing physical matrix annihilation for block generation.\n")

class SovereignAuraChain:
    def __init__(self):
        self.chain = []
        self.chain.append({"index": 1, "proof": "GENESIS", "science_output": "NULL"})

    def mine_scientific_block(self, target_script):
        # Explicitly path to your Aperture-7 workspace
        workspace = os.path.expanduser("~/aperture_workspace")
        script_path = os.path.join(workspace, target_script)
        
        print(f"[!] INITIATING SPATIAL COMPUTE: {target_script}...")
        
        try:
            # Execute the bare-metal Python physics script
            result = subprocess.run(
                ["python3", script_path], 
                capture_output=True, text=True, check=True, cwd=workspace
            )
            raw_math_output = result.stdout.strip()
            
            print(f"    -> Engine Output:\n       {raw_math_output}")
            
            # Hash the scientific result to lock the block
            block_proof = hashlib.sha256(raw_math_output.encode()).hexdigest()
            print(f"    -> CRYPTOGRAPHIC PROOF GENERATED: 0x{block_proof[:16]}")
            
            new_block = {
                "index": len(self.chain) + 1,
                "timestamp": time.time(),
                "science_output": raw_math_output,
                "proof": block_proof
            }
            self.chain.append(new_block)
            print(f"[+] BLOCK {new_block['index']} MINED VIA APERTURE-7 COMPUTE.\n")
            
        except subprocess.CalledProcessError as e:
            print(f"[!] COMPUTE FAILED. Engine exited with code {e.returncode}.")
        except FileNotFoundError:
            print(f"[!] ERROR: {script_path} is missing from the workspace.")

live_chain = SovereignAuraChain()
time.sleep(1)

# Mine Block 2 using the Cayley-Hamilton Annihilation
live_chain.mine_scientific_block("boss2_cayley.py")
time.sleep(1)

# Mine Block 3 using Fourier vs Bare-Metal LU Determinants
live_chain.mine_scientific_block("brink1_duality.py")
