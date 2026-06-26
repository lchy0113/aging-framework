# aging-framework

SmartThings API 기반 전원 제어와 UART/ADB 로그 감시를 조합해 Aging Test를 수행하는 Python Framework.

## 1. venv 구성

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 설정

`config/config.yaml`에 SmartThings token, device_id, serial port 설정.


```yaml
smartthings:
  ssl:
    verify: false
    ca_cert: null
```

정상 CA 인증서를 사용할 경우:

```yaml
smartthings:
  ssl:
    verify: true
    ca_cert: "./certs/xxxxxxxxxx.crt"
```

## 3. PowerController 테스트

```bash
python scripts/test_power.py
```

## 4. Basic Power Cycle

```bash
python main.py --scenario basic_power_cycle
```

## 5. Serial 단독 테스트

```bash
python scripts/test_serial.py
```

## 6. ILITEK Boot Aging

```bash
python main.py --scenario ilitek_boot
```

## Report

결과는 `reports/` 아래 CSV로 저장.

## Logs

- `logs/raw/`: 회차별 UART 원본 로그
- `logs/fail/`: 실패 회차 로그
