import os
from pathlib import Path

import yaml


class Config:
    def __init__(self, config_path="config/config.yaml"):

        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}"
            )

        with self.config_path.open("r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        cur = self.data

        for key in keys:
            if not isinstance(cur, dict) or key not in cur:
                return default
            cur = cur[key]

        return cur

    # -------------------------------------------------------
    # SmartThings
    # -------------------------------------------------------

    def smartthings_token(self):
        token = os.getenv("SMARTTHINGS_TOKEN")

        if not token:
            raise RuntimeError(
                "SMARTTHINGS_TOKEN not found.\n"
                "Please create config/.env\n"
                "Example:\n"
                "SMARTTHINGS_TOKEN=xxxxxxxxxxxxxxxx"
            )

        return token

    def ssl_verify(self):
        return self.get(
            "smartthings",
            "ssl",
            "verify",
            default=True,
        )

    def ca_cert(self):
        return self.get(
            "smartthings",
            "ssl",
            "ca_cert",
        )

    def device_id(self, name):
        env_name = f"SMARTTHINGS_{name.upper()}_DEVICE_ID"

        device_id = os.getenv(env_name)

        if device_id:
            return device_id

        raise RuntimeError(
            f"{env_name} not found.\n"
            "Please create config/.env"
        )

    def device_component(self, name):
        return self.get(
            "smartthings",
            "devices",
            name,
            "component",
            default="main",
        )