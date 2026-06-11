import os
import sys
import subprocess
import json
import time
import glob
import shutil

class BobcoinNodeClient:
    """
    v5.0.0 Bobcoin Node Client.
    Enhanced with robust CLI discovery, persistent queuing, and 'mint watcher'.
    """
    def __init__(self, cli_path=None):
        self.cli_path = self._discover_cli(cli_path)
        self.queue_path = "logs/transaction_queue.json"
        self.request_dir = "logs/mint_requests"
        os.makedirs(self.request_dir, exist_ok=True)

    def _load_queue(self):
        if os.path.exists(self.queue_path):
            try:
                with open(self.queue_path, 'r') as f: return json.load(f)
            except Exception: return []
        return []

    def _save_queue(self, queue):
        os.makedirs(os.path.dirname(self.queue_path), exist_ok=True)
        with open(self.queue_path, 'w') as f:
            json.dump(queue, f, indent=2)

    def _discover_cli(self, provided_path):
        """v5.0.0 Robust CLI path discovery for standard Linux distros."""
        paths = [
            provided_path,
            "extern/bobcoin/bobcoin-cli",
            "extern/bobcoin/bin/bobcoin-cli",
            "/usr/local/bin/bobcoin-cli",
            "/usr/bin/bobcoin-cli",
            os.path.expanduser("~/bin/bobcoin-cli")
        ]
        for p in paths:
            if p and os.path.exists(p) and os.access(p, os.X_OK):
                print(f"  [Bobcoin] Discovered CLI at: {p}")
                return p

        system_path = shutil.which("bobcoin-cli")
        if system_path:
            print(f"  [Bobcoin] Discovered CLI in PATH: {system_path}")
            return system_path

        print("  [Bobcoin] WARNING: Bobcoin CLI not found. Node features may fail.")
        return provided_path or "bobcoin-cli"

    def node_heartbeat(self):
        """Checks if the bobcoin node is responding."""
        try:
            subprocess.run([self.cli_path, "ping"], check=True, capture_output=True)
            return True
        except Exception:
            return False

    def mint_fitness_reward(self, calories, duration_sec):
        reward = round((calories / 100.0) + (duration_sec / 60.0) * 0.1, 2)
        print(f"  [Bobcoin] Calculated Reward: {reward} BOB")

        try:
            if not self.node_heartbeat(): raise ConnectionError("Node unreachable")

            subprocess.run([self.cli_path, "mint", str(reward)], check=True)
            print(f"  [Bobcoin] Node Online: Successfully minted {reward} BOB.")
            self.flush_queue()
            return True
        except Exception as e:
            print(f"  [Bobcoin] Node Offline/Error ({e}): Queuing {reward} BOB for later.")
            queue = self._load_queue()
            queue.append({
                "timestamp": time.ctime(),
                "reward": reward,
                "retry_count": 0
            })
            self._save_queue(queue)
            return False

    def flush_queue(self):
        """Attempts to process all queued transactions."""
        queue = self._load_queue()
        if not queue: return

        if not self.node_heartbeat():
            return

        print(f"  [Bobcoin] Connection Restored: Flushing {len(queue)} transactions...")
        remaining = []
        for tx in queue:
            try:
                subprocess.run([self.cli_path, "mint", str(tx["reward"])], check=True)
            except Exception:
                tx["retry_count"] += 1
                if tx["retry_count"] < 10: # Limit retries
                    remaining.append(tx)

        self._save_queue(remaining)

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
