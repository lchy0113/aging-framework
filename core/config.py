import yaml
from pathlib import Path


class Config:
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        cur = self.data
        for key in keys:
            if not isinstance(cur, dict) or key not in cur:
                return default
            cur = cur[key]
        return cur

    def smartthings_token(self):
        return self.get("smartthings", "token")

    def ssl_verify(self):
        return self.get("smartthings", "ssl", "verify", default=True)

    def ca_cert(self):
        return self.get("smartthings", "ssl", "ca_cert")

    def device_id(self, name):
        return self.get("smartthings", "devices", name, "device_id")

    def device_component(self, name):
        return self.get("smartthings", "devices", name, "component", default="main")
