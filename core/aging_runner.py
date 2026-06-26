import time
from datetime import datetime

from .report import Report


class AgingRunner:
    def __init__(self, config, scenario):
        self.config = config
        self.scenario = scenario
        self.max_count = config.get("aging", "max_count", default=1)
        self.interval_sec = config.get("aging", "interval_sec", default=0)
        self.stop_on_fail = config.get("aging", "stop_on_fail", default=True)
        self.report = Report(scenario.name)

    def run(self):
        print(f"[AgingRunner] scenario={self.scenario.name}")
        print(f"[AgingRunner] max_count={self.max_count}")

        self.scenario.setup()

        try:
            for index in range(1, self.max_count + 1):
                started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{index:04d}] START {started_at}")

                result = self.scenario.run_once(index)
                self.report.add(index, result)

                if result.passed:
                    print(f"[{index:04d}] PASS: {result.reason}")
                else:
                    print(f"[{index:04d}] FAIL: {result.reason}")
                    if self.stop_on_fail:
                        break

                if self.interval_sec > 0:
                    time.sleep(self.interval_sec)

        finally:
            self.scenario.teardown()
            path = self.report.save()
            print(f"[AgingRunner] report saved: {path}")
