class SmartPlug:
    def __init__(self, client, device_id, component="main"):
        self.client = client
        self.device_id = device_id
        self.component = component

    def on(self):
        return self._send_switch_command("on")

    def off(self):
        return self._send_switch_command("off")

    def _send_switch_command(self, command):
        if command not in ("on", "off"):
            raise ValueError(f"Invalid switch command: {command}")

        payload = {
            "commands": [
                {
                    "component": self.component,
                    "capability": "switch",
                    "command": command,
                }
            ]
        }

        return self.client.post(f"/devices/{self.device_id}/commands", payload)
