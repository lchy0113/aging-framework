import csv
from pathlib import Path
from datetime import datetime


class Report:
    def __init__(self, scenario_name):
        self.scenario_name = scenario_name
        self.rows = []

    def add(self, index, result):
        self.rows.append({
            "index": index,
            "scenario": self.scenario_name,
            "result": "PASS" if result.passed else "FAIL",
            "reason": result.reason,
            "fail_pattern": result.fail_pattern or "",
            "log_file": result.log_file or "",
            "start_time": result.start_time or "",
            "end_time": result.end_time or "",
            "duration_sec": result.duration_sec if result.duration_sec is not None else "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    def save(self):
        report_dir = Path("reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{self.scenario_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = report_dir / filename

        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "index",
                    "scenario",
                    "result",
                    "reason",
                    "fail_pattern",
                    "log_file",
                    "start_time",
                    "end_time",
                    "duration_sec",
                    "timestamp",
                ],
            )
            writer.writeheader()
            writer.writerows(self.rows)

        return path
