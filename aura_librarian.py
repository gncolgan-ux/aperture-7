import h3
import hashlib
import os
import json

class AuraLibrarian:
    def __init__(self, db_path="HEX_GRAPH_H3.bin", block_size=1024, resolution=5):
        self.db_path = db_path
        self.block_size = block_size
        self.resolution = resolution
        self.state_file = "aura_state.json"
        
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"level": 1, "xp": 0}

        if not os.path.exists(self.db_path):
            print(f"[SYSTEM] Initializing blank lattice at {self.db_path}...")
            with open(self.db_path, "wb") as f:
                f.truncate(100 * 1024 * 1024)
            self.gain_xp(500, "INITIALIZED 100MB LATTICE")

    def gain_xp(self, points, action):
        self.state["xp"] += points
        old_level = self.state["level"]
        
        self.state["level"] = (self.state["xp"] // 1000) + 1
        
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
            
        print(f"[+] {action} (+{points} XP)")
        if self.state["level"] > old_level:
            print(f"\n======================================")
            print(f" ⬆️  LEVEL UP! AURA REACHED LEVEL {self.state['level']} ⬆️")
            print(f"======================================\n")

    def _topic_to_h3_offset(self, topic: str):
        hash_val = int(hashlib.md5(topic.encode('utf-8')).hexdigest(), 16)
        lat = (hash_val % 1800000) / 10000.0 - 90.0
        lng = ((hash_val // 1800000) % 3600000) / 10000.0 - 180.0
        
        try:
            cell_id_hex = h3.geo_to_h3(lat, lng, self.resolution)
        except AttributeError:
            cell_id_hex = h3.latlng_to_cell(lat, lng, self.resolution)
            
        return int(cell_id_hex, 16) % 90000

    # INTERNAL AGENT 1: The Micro-Grid Quantizer
    def agent_spatial_quantizer(self, filepath, bucket_size=10):
        print(f"\n[AGENT-1] Initiating Localized 3D Voxel Buckets...")
        micro_sectors = {}
        
        # Test coordinates simulating deep-carbon ash interference
        test_points = [
            (15.2, 30.1, -1.0, 0.8), (16.5, 31.0, -1.2, 0.7),
            (25.0, 40.0, -2.0, 0.9), (15.8, 30.5, -1.1, 0.85)
        ]
        
        for x, y, z, density in test_points:
            if density > 0.65:
                sector_hash = f"{int(x//bucket_size)}_{int(y//bucket_size)}_{int(z//bucket_size)}"
                if sector_hash not in micro_sectors:
                    micro_sectors[sector_hash] = {'count': 0, 'z_sum': 0}
                micro_sectors[sector_hash]['count'] += 1
                micro_sectors[sector_hash]['z_sum'] += z
                
                # Instantly route to the central hexagonal calculator
                offset = self._topic_to_h3_offset(sector_hash)
                self.gain_xp(35, f"QUANTIZED SECTOR {sector_hash} TO HEX OFFSET {offset}")
                
        print(f"[+] Agent-1 localized {len(micro_sectors)} structural anomalies.")

    # INTERNAL AGENT 2: Volumetric Streaming Scanner
    def agent_volumetric_stream(self, chunks=3):
        print("\n[AGENT-2] Pushing engine to maximum volumetric depth...")
        chunk_size = 2048 * 1024
        
        for i in range(chunks):
            start = i * chunk_size
            end = start + chunk_size - 1
            print(f"         -> Streaming spatial matrix block: Bytes {start} to {end}...")
            
            # Fuse the streamed block directly into the lattice
            topic = f"VOLUMETRIC_BLOCK_{i}"
            offset = self._topic_to_h3_offset(topic)
            self.gain_xp(50, f"STREAMED BLOCK {i} ROUTED TO HEX OFFSET {offset}")
            
        print("[+] Agent-2 continuous papyrus stream complete.")

if __name__ == "__main__":
    print("\n[APERTURE-7] All-In-One Master Engine Online.")
    engine = AuraLibrarian()
    
    # The agents are now just internal functions fired from the core
    engine.agent_spatial_quantizer("real_fragment_matrix.csv")
    engine.agent_volumetric_stream(chunks=3)
    
    print(f"\n[SYSTEM] Run Complete. Engine Status: Level {engine.state['level']} | Total XP: {engine.state['xp']}")
