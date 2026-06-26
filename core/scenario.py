from abc import ABC, abstractmethod


class ScenarioResult:
    def __init__(
        self,
        passed,
        reason="",
        log_file=None,
        fail_pattern=None,
        start_time=None,
        end_time=None,
        duration_sec=None,
    ):
        self.passed = passed
        self.reason = reason
        self.log_file = log_file
        self.fail_pattern = fail_pattern
        self.start_time = start_time
        self.end_time = end_time
        self.duration_sec = duration_sec

    @classmethod
    def pass_result(cls, reason="PASS", log_file=None, **kwargs):
        return cls(True, reason, log_file, **kwargs)

    @classmethod
    def fail_result(cls, reason="FAIL", log_file=None, **kwargs):
        return cls(False, reason, log_file, **kwargs)


class Scenario(ABC):
    name = "base"

    def __init__(self, config, power):
        self.config = config
        self.power = power

    def setup(self):
        pass

    @abstractmethod
    def run_once(self, index):
        pass

    def teardown(self):
        pass
