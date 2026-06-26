import requests
import urllib3
from pathlib import Path


class SmartThingsClient:
    BASE_URL = "https://api.smartthings.com/v1"

    def __init__(self, token, ssl_verify=True, ca_cert=None, timeout=10):
        self.token = token
        self.timeout = timeout
        self.verify = self._resolve_verify(ssl_verify, ca_cert)

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _resolve_verify(self, ssl_verify, ca_cert):
        if ssl_verify is False:
            return False

        if ca_cert:
            ca_cert_path = Path(ca_cert)

            if not ca_cert_path.is_absolute():
                project_root = Path(__file__).resolve().parents[1]
                ca_cert_path = project_root / ca_cert_path

            if not ca_cert_path.exists():
                raise FileNotFoundError(f"CA certificate not found: {ca_cert_path}")

            return str(ca_cert_path)

        return True

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def request(self, method, path, payload=None):
        response = requests.request(
            method=method,
            url=f"{self.BASE_URL}{path}",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
            verify=self.verify,
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(
                f"SmartThings API failed: method={method}, path={path}, "
                f"status={response.status_code}, body={response.text}"
            )

        return response.json() if response.text else {}

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, payload):
        return self.request("POST", path, payload)
