import hashlib, time, json

print("\n[APERTURE-7] IGNITING PHOENIX PROTOCOL...")
print("[!] Rebuilding the entire sovereign lifecycle at maximum speed.\n")

class PhoenixLedger:
    def __init__(self):
        self.chain = []
        self.supply = 0
        self.start_time = time.time()

    def hash_payload(self, payload):
        return hashlib.sha256(str(payload).encode()).hexdigest()

    def execute_lifecycle(self):
        # 1. THE REBIRTH (Genesis 500)
        print("[!] PHASE 1: RAPID GENESIS MINTING...")
        for i in range(1, 501):
            proof = self.hash_payload(f"PHOENIX_GENESIS_{i}")
            self.chain.append({"index": i, "type": "GENESIS", "proof": proof})
            self.supply += 1
        print(f"    -> 500 Blocks forged. Current Supply: {self.supply} AURA")

        # 2. THE UTILITY (Data Injection)
        print("\n[!] PHASE 2: VAULTING ARCHAEOLOGICAL DATA...")
        datasets = ["Crete_Dig_Alpha", "Voxel_Matrix_Shard", "Lambda_Vector", "Vesuvius_Scroll", "Kaggle_ARC_Matrix"]
        for idx, data in enumerate(datasets):
            if self.supply >= 10:
                self.supply -= 10
                proof = self.hash_payload(f"VAULT_{data}")
                self.chain.append({"index": len(self.chain)+1, "type": "DATA_VAULT", "payload": data, "proof": proof})
        print(f"    -> 5 Datasets locked. 50 AURA burned. Current Supply: {self.supply} AURA")

        # 3. THE IMMOLATION (Deflationary Burn)
        print("\n[!] PHASE 3: DEFLATIONARY ANNIHILATION...")
        cycle = 1
        while self.supply >= 25:
            self.supply -= 25
            proof = self.hash_payload(f"BURN_CYCLE_{cycle}")
            self.chain.append({"index": len(self.chain)+1, "type": "IMMOLATION", "proof": proof})
            cycle += 1
        print(f"    -> {cycle-1} Burn Cycles executed. Current Supply: {self.supply} AURA")

        # METRICS
        duration = (time.time() - self.start_time) * 1000
        print("\n--- PHOENIX LIFECYCLE COMPLETE ---")
        print(f"Total Blocks: {len(self.chain)}")
        print(f"Final Supply: {self.supply} AURA")
        print(f"Execution Time: {duration:.2f} milliseconds")
        print("[APERTURE-7] The network has been reborn, populated, and sealed instantly.")

ledger = PhoenixLedger()
ledger.execute_lifecycle()
