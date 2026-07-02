import requests
import urllib3
import time
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
        print(f"[SmartThings] {method} {path}")

        try:
            response = requests.request(
                method=method,
                url=f"{self.BASE_URL}{path}",
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
                verify=self.verify,
            )
        except requests.exceptions.Timeout:
            raise RuntimeError(
                "SmartThings API Timeout\n"
                "네트워크 상태 또는 SmartThings 서버 응답 상태를 확인하세요."
            )
        except requests.exceptions.SSLError as e:
            raise RuntimeError(f"SmartThings SSL Error\n{e}")
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(f"SmartThings Connection Error\n{e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"SmartThings Request Error\n{e}")

        print(f"[SmartThings] status={response.status_code}")

        if response.status_code == 401:
            raise RuntimeError(
                "\n"
                "========================================\n"
                " SmartThings Authentication Failed\n"
                "========================================\n"
                "Status : 401 Unauthorized\n\n"
                "Personal Access Token(PAT)이 만료되었거나 유효하지 않습니다.\n\n"
                "1. https://account.smartthings.com/tokens\n"
                "2. 새로운 Personal Access Token 생성\n"
                "3. config/config.yaml 의 smartthings.token 값 변경\n"
                "4. python3 scripts/test_plug.py 로 먼저 확인\n"
            )

        if response.status_code == 403:
            raise RuntimeError(
                "SmartThings Permission Denied (403)\n"
                "PAT 권한이 부족하거나 해당 Device에 접근 권한이 없습니다.\n"
                "Device Read / Execute Commands 권한을 확인하세요.\n"
                f"path={path}\n"
                f"body={response.text}"
            )

        if response.status_code == 404:
            raise RuntimeError(
                "SmartThings Device Not Found (404)\n"
                "config/config.yaml의 smartthings.device_id 값을 확인하세요.\n"
                f"path={path}\n"
                f"body={response.text}"
            )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            wait_sec = 5
            if retry_after:
                try:
                    wait_sec = int(retry_after)
                except ValueError:
                    pass
            
            raise RuntimeError(
                "SmartThings API Rate Limit Exceeded (429)\n"
                f"API 호출제한에 걸렸습니다. {wait_sec}초 이상 대기 후 재시도 하세요.\n"
                f"body={response.text}"
            )

        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(
                "SmartThings API failed\n"
                f"method : {method}\n"
                f"path   : {path}\n"
                f"status : {response.status_code}\n"
                f"body   : {response.text}"
            )

        return response.json() if response.text else {}

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, payload):
        return self.request("POST", path, payload)