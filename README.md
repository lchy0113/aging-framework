# aging-framework

SmartThings API 기반 전원 제어와 UART/ADB 로그 감시를 조합하여 Android Embedded Platform의 Aging Test를 수행하는 Python Framework.

현재 지원하는 Scenario

- Basic Power Cycle
- ILITEK Boot Aging
- eMMC Storage Aging

---

# 1. Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# 2. SmartThings 설정

## config/.env 생성

```bash
SMARTTHINGS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SMARTTHINGS_MAIN_PLUG_DEVICE_ID=e5ea13c4-6697-4d98-a750-86c3539a0c9e
```

`.env` 파일은 Git에 Commit하지 않는다.

---

## config/config.yaml

SmartThings SSL 및 시험 환경만 설정한다.

```yaml
smartthings:
  ssl:
    verify: false
    ca_cert: null

power:
  controller: smartthings
  device: main_plug
```

CA 인증서를 사용하는 경우

```yaml
smartthings:
  ssl:
    verify: true
    ca_cert: "./certs/KDONE_SSL_CERT.crt"
```

---

# 3. SmartPlug 테스트

```bash
python3 scripts/test_plug.py
```

예상 결과

```
[TEST] Power OFF
[SmartThings] status=200
[TEST] Power ON
[SmartThings] status=200
```

---

# 4. Scenario 실행

## Basic Power Cycle

```bash
python3 main.py --scenario basic_power_cycle
```

---

## ILITEK Boot Aging

```bash
python3 main.py --scenario ilitek_boot
```

---

## eMMC Storage Aging

```bash
python3 main.py --scenario emmc_storage
```

현재 수행 항목

- SmartPlug Power OFF / ON
- Android Boot Complete 확인
- eMMC Device 정보 수집
- Read / Write Verify
- SHA-256 무결성 확인
- Kernel Storage Error 검사
- CSV Report 저장

---

# 5. Utility

## Serial Monitor

```bash
python3 scripts/test_serial.py
```

---

## SmartPlug Test

```bash
python3 scripts/test_plug.py
```

---

# 6. Report

시험 결과는 `reports/`에 CSV 형식으로 저장된다.

예

```
reports/
 ├── basic_power_cycle_xxxxx.csv
 ├── ilitek_boot_xxxxx.csv
 └── emmc_storage_xxxxx.csv
```

---

# 7. Log

```
logs/
 ├── raw/
 └── fail/
```

- **raw/** : 회차별 원본 로그
- **fail/** : FAIL 발생 시 로그

---

# 8. eMMC Storage Scenario

현재 검증 항목

- Cold Boot
- SmartPlug Power Cycle
- eMMC Device Information
- SHA-256 Data Integrity
- Read / Write Test
- Kernel Storage Error Detection

향후 추가 예정

- Random Power Cut During Write
- Long Write Stress
- Boot Time Trend Analysis
- eMMC Health Monitoring
- Factory Reset Test
- OTA Validation