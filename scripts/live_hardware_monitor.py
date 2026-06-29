import time
import os

def main():
    print("[FCDM Monitor] Live Hardware Monitor Initialized.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[FCDM Monitor] Exiting.")

if __name__ == "__main__":
    main()
