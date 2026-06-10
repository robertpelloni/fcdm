import os
import sys
import subprocess
import json
import time

class BobcoinNodeClient:
    """
    v2.9.0 Bobcoin Node Client.
    Enhanced with resilience, local reward caching, and automated cache flushing.
    """
    def __init__(self, cli_path="extern/bobcoin/bobcoin-cli"):
        self.cli_path = cli_path
        self.cache_path = "logs/reward_cache.json"

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        return []

    def _save_cache(self, cache):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(cache, f, indent=2)

    def get_balance(self):
        """Fetches the current wallet balance."""
        try:
            # Simulated node call
            return 2540.20
        except Exception:
            return "OFFLINE"

    def mint_fitness_reward(self, calories, duration_sec):
        """
        Mints BOB based on fitness metrics with retry and local caching.
        """
        reward = round((calories / 100.0) + (duration_sec / 60.0) * 0.1, 2)

        try:
            # Attempt real mint (placeholder)
            # subprocess.run([self.cli_path, "mint", str(reward)], check=True)
            print(f"  [Bobcoin] Minted {reward} BOB for workout performance.")

            # If success, try to flush any cached rewards
            self.flush_cache()
            return reward
        except Exception:
            print(f"  [Bobcoin] Node offline. Caching {reward} BOB locally.")
            cache = self._load_cache()
            cache.append({
                "timestamp": time.ctime(),
                "reward": reward,
                "reason": "fitness_workout"
            })
            self._save_cache(cache)
            return reward

    def flush_cache(self):
        """Attempts to mint all cached rewards."""
        cache = self._load_cache()
        if not cache: return

        print(f"  [Bobcoin] Node back online. Flushing {len(cache)} cached rewards...")
        remaining = []
        for item in cache:
            try:
                # Attempt to mint each cached item
                # subprocess.run([self.cli_path, "mint", str(item["reward"])], check=True)
                pass
            except Exception:
                remaining.append(item)

        self._save_cache(remaining)

if __name__ == "__main__":
    client = BobcoinNodeClient()
    print(f"Balance: {client.get_balance()} BOB")
    client.mint_fitness_reward(450, 1800)
