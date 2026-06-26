class SmartThingsDevice:
    def __init__(self, client):
        self.client = client

    def list_devices(self):
        return self.client.get("/devices")

    def get_status(self, device_id):
        return self.client.get(f"/devices/{device_id}/status")
