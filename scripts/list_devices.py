import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.config import Config
from smartthings import SmartThingsClient, SmartThingsDevice


def main():
    config = Config(ROOT_DIR / "config" / "config.yaml")

    client = SmartThingsClient(
        config.smartthings_token(),
        ssl_verify=config.ssl_verify(),
        ca_cert=config.ca_cert(),
    )

    device = SmartThingsDevice(client)
    result = device.list_devices()

    for item in result.get("items", []):
        print(f'{item.get("label")} | {item.get("name")} | {item.get("deviceId")}')


if __name__ == "__main__":
    main()
