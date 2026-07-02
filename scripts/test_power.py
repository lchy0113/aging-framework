import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
load_dotenv("config/.env")

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.config import Config
from controllers import create_power_controller


def main():
    config = Config(ROOT_DIR / "config" / "config.yaml")
    power = create_power_controller(config)

    print("[TEST] Power OFF")
    power.power_off()

    time.sleep(5)

    print("[TEST] Power ON")
    power.power_on()

    print("[TEST] Done")


if __name__ == "__main__":
    main()
