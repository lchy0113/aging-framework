import time
from datetime import datetime

from core.scenario import Scenario, ScenarioResult
from core.logger import make_log_path
from monitors.serial_monitor import SerialMonitor
from monitors.pattern_checker import PatternChecker


class IlitekBootScenario(Scenario):
    name = "ilitek_boot"

    def setup(self):
        self.monitor = SerialMonitor(
            port=self.config.get("serial", "port"),
            baudrate=self.config.get("serial", "baudrate", default=115200),
            timeout_sec=self.config.get("serial", "timeout_sec", default=1),
        )
        self.monitor.open()

        self.checker = PatternChecker(
            fail_patterns=self.config.get("ilitek", "fail_patterns", default=[]),
            pass_patterns=self.config.get("ilitek", "pass_patterns", default=[]),
            ignore_case=False,
        )

    def run_once(self, index):
        start_dt = datetime.now()
        start_time = start_dt.strftime("%Y-%m-%d %H:%M:%S")

        off_delay = self.config.get("aging", "power_off_delay_sec", default=5)
        boot_wait = self.config.get("aging", "boot_wait_sec", default=0)
        boot_timeout = self.config.get("ilitek", "boot_timeout_sec", default=90)

        print(f"[{index:04d}] Power OFF")
        self.power.power_off()
        time.sleep(off_delay)

        log_path = make_log_path("raw", "ilitek", index)

        print(f"[{index:04d}] UART flush")
        self.monitor.flush_input()

        print(f"[{index:04d}] Power ON")
        self.power.power_on()

        if boot_wait > 0:
            time.sleep(boot_wait)

        print(f"[{index:04d}] Collect UART logs: timeout={boot_timeout}s")
        collected = self.monitor.collect_until(
            timeout_sec=boot_timeout,
            log_path=log_path,
            checker=self.checker,
        )

        end_dt = datetime.now()
        end_time = end_dt.strftime("%Y-%m-%d %H:%M:%S")
        duration_sec = round((end_dt - start_dt).total_seconds(), 3)

        if collected["passed"]:
            return ScenarioResult.pass_result(
                collected["reason"],
                str(log_path),
                start_time=start_time,
                end_time=end_time,
                duration_sec=duration_sec,
            )

        fail_log = make_log_path("fail", "ilitek_fail", index)
        fail_log.write_text(
            log_path.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )

        return ScenarioResult.fail_result(
            collected["reason"],
            str(fail_log),
            fail_pattern=collected["fail_pattern"],
            start_time=start_time,
            end_time=end_time,
            duration_sec=duration_sec,
        )

    def teardown(self):
        self.monitor.close()
