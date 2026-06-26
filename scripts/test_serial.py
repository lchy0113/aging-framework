import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.config import Config
from monitors.serial_monitor import SerialMonitor


def main():
    config = Config(ROOT_DIR / "config" / "config.yaml")

    monitor = SerialMonitor(
        port=config.get("serial", "port"),
        baudrate=config.get("serial", "baudrate", default=115200),
        timeout_sec=config.get("serial", "timeout_sec", default=1),
    )

    print("[TEST] Open serial")
    monitor.open()

    print("[TEST] Read 10 lines")
    try:
        for _ in range(10):
            raw = monitor.ser.readline()
            if raw:
                print(raw.decode("utf-8", errors="replace"), end="")
    finally:
        monitor.close()
        print("\n[TEST] Done")


if __name__ == "__main__":
    main()
