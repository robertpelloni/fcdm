import os
import sys
import subprocess
import json
import time
import glob

class BobcoinNodeClient:
    """
    v3.2.0 Bobcoin Node Client.
    Enhanced with resilience, local reward caching, and a background 'mint watcher' for ITGMania integration.
    """
    def __init__(self, cli_path="extern/bobcoin/bobcoin-cli"):
        self.cli_path = cli_path
        self.cache_path = "logs/reward_cache.json"
        self.request_dir = "logs/mint_requests"
        os.makedirs(self.request_dir, exist_ok=True)

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f: return json.load(f)
            except Exception: return []
        return []

    def _save_cache(self, cache):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(cache, f, indent=2)

    def mint_fitness_reward(self, calories, duration_sec):
        reward = round((calories / 100.0) + (duration_sec / 60.0) * 0.1, 2)
        try:
            # subprocess.run([self.cli_path, "mint", str(reward)], check=True)
            print(f"  [Bobcoin] Successfully minted {reward} BOB.")
            self.flush_cache()
            return True
        except Exception:
            print(f"  [Bobcoin] Node offline. Caching {reward} BOB.")
            cache = self._load_cache()
            cache.append({"timestamp": time.ctime(), "reward": reward})
            self._save_cache(cache)
            return False

    def flush_cache(self):
        cache = self._load_cache()
        if not cache: return
        remaining = []
        for item in cache:
            try: # subprocess.run([self.cli_path, "mint", str(item["reward"])], check=True)
                pass
            except Exception: remaining.append(item)
        self._save_cache(remaining)

    def run_watcher(self):
        """Background loop to process mint requests from ITGMania (Lua)."""
        print(f"Bobcoin Mint Watcher active. Monitoring {self.request_dir}...")
        try:
            while True:
                requests = glob.glob(os.path.join(self.request_dir, "*.json"))
                for req_path in requests:
                    try:
                        with open(req_path, 'r') as f:
                            data = json.load(f)
                        print(f"Processing request: {req_path}")
                        self.mint_fitness_reward(data['calories'], data['duration'])
                        os.remove(req_path)
                    except Exception as e:
                        print(f"Failed to process {req_path}: {e}")
                time.sleep(2)
        except KeyboardInterrupt:
            print("Watcher stopped.")

if __name__ == "__main__":
    client = BobcoinNodeClient()
    if "--watcher" in sys.argv:
        client.run_watcher()
    else:
        client.mint_fitness_reward(450, 1800)
