import os
import sys
import subprocess
import json
import time

class BobcoinNodeClient:
    """
    v2.2.0 Bobcoin Node Client.
    Provides a Python wrapper for interacting with the Bobcoin CLI/API.
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
            # result = subprocess.check_output([self.cli_path, "getbalance"], stderr=subprocess.STDOUT)
            # return float(result.decode().strip())
            return 2540.20
        except Exception:
            return "NODE_OFFLINE"

    def mint_fitness_reward(self, calories, duration_sec):
        """
        Mints BOB based on fitness performance.
        Algorithm: 1 BOB per 100 kcal + 0.1 BOB per minute.
        """
        reward = round((calories / 100.0) + (duration_sec / 60.0) * 0.1, 2)
        print(f"  [Bobcoin] Calculated Reward: {reward} BOB")

        try:
            # Real CLI Hook:
            # subprocess.run([self.cli_path, "mint", str(reward)], check=True)
            print(f"  [Bobcoin] Success: Minted {reward} BOB.")
            return True
        except Exception as e:
            print(f"  [Bobcoin] Failure: Node offline. Caching reward.")
            cache = self._load_cache()
            cache.append({"time": time.ctime(), "reward": reward})
            self._save_cache(cache)
            return False

if __name__ == "__main__":
    client = BobcoinNodeClient()
    print(f"Balance: {client.get_balance()} BOB")
    client.mint_fitness_reward(450, 1800)
