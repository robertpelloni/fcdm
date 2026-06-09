import os
import sys
import subprocess
import json

class BobcoinNodeClient:
    """
    v2.0.0 Bobcoin Node Client.
    Provides a Python wrapper for interacting with the Bobcoin supernode.
    """
    def __init__(self, cli_path="extern/bobcoin/bobcoin-cli"):
        self.cli_path = cli_path

    def get_balance(self):
        """Fetches the current wallet balance."""
        # Simulated node interaction
        return 2540.20

    def mint_fitness_reward(self, calories, duration_sec):
        """
        Mints BOB based on fitness metrics.
        Fitness Mining: 1 BOB per 100 kcal + 0.1 BOB per minute.
        """
        reward = (calories / 100.0) + (duration_sec / 60.0) * 0.1
        reward = round(reward, 2)

        # In production, this calls the local supernode
        # cmd = [self.cli_path, "mint", str(reward)]
        # subprocess.run(cmd, check=True)

        print(f"  [Bobcoin] Minted {reward} BOB for workout performance.")
        return reward

if __name__ == "__main__":
    client = BobcoinNodeClient()
    print(f"Balance: {client.get_balance()} BOB")
    client.mint_fitness_reward(450, 1800)
