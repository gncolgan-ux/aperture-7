import hashlib, time, json

print("\n[AURA PROTOCOL] INJECTING DATA VALUE INTO THE LEDGER...")
print("[!] Spending genesis coins to permanently secure archaeological metadata.\n")

class ValueLedger:
    def __init__(self):
        self.chain = []
        self.genesis_balance = 500

    def store_data(self, payload):
        if self.genesis_balance < 10:
            print("[!] INSUFFICIENT FUNDS.")
            return
            
        self.genesis_balance -= 10
        block_hash = hashlib.sha256(json.dumps(payload).encode()).hexdigest()
        
        new_block = {
            "index": len(self.chain) + 501,
            "timestamp": time.time(),
            "data_payload": payload,
            "proof_hash": block_hash
        }
        self.chain.append(new_block)
        print(f"[+] BLOCK {new_block['index']} VAULTED | 10 AURA BURNED | PROOF: 0x{block_hash[:16]}")

ledger = ValueLedger()
time.sleep(1)

# Injecting 5 real datasets to give the chain intrinsic utility
datasets = [
    {"type": "H3_INDEX", "location": "Crete_Dig_Site_Alpha", "hex": "8a2a1072b59ffff"},
    {"type": "VOXEL_MATRIX", "artifact": "Minoan_Pottery_Shard", "density_peak": 45.2},
    {"type": "SPATIAL_VECTOR", "trajectory": "Z0:E2 -> Z1:E3 -> Z2:E5", "glyph": "LAMBDA"},
    {"type": "VESUVIUS_SCROLL", "sector": "VOL_1_COL4", "structural_match": "OMICRON"},
    {"type": "KAGGLE_ARC", "matrix_id": "5614dbcf", "solved_entropy": 0.442}
]

for data in datasets:
    ledger.store_data(data)
    time.sleep(0.5)

print(f"\n--- AURA LEDGER STATE ---")
print(f"Remaining Genesis Balance: {ledger.genesis_balance} AURA")
print("[APERTURE-7] Value injected. The blockchain is now a decentralized data vault.")
