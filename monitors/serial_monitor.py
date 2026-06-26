import time
import serial


class SerialMonitor:
    def __init__(self, port, baudrate=115200, timeout_sec=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout_sec = timeout_sec
        self.ser = None

    def open(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout_sec,
        )

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def flush_input(self):
        if self.ser is None or not self.ser.is_open:
            self.open()
        self.ser.reset_input_buffer()

    def collect_until(self, timeout_sec, log_path, checker=None):
        if self.ser is None or not self.ser.is_open:
            self.open()

        start = time.time()
        matched_fail_pattern = None
        matched_pass_pattern = None
        line_count = 0

        with open(log_path, "w", encoding="utf-8", errors="replace") as f:
            while time.time() - start < timeout_sec:
                raw = self.ser.readline()
                if not raw:
                    continue

                line = raw.decode("utf-8", errors="replace")
                line_count += 1

                print(line, end="")
                f.write(line)
                f.flush()

                if checker:
                    fail_pattern = checker.find_fail(line)
                    if fail_pattern:
                        matched_fail_pattern = fail_pattern
                        return {
                            "passed": False,
                            "reason": f"fail pattern detected: {fail_pattern}",
                            "fail_pattern": matched_fail_pattern,
                            "pass_pattern": matched_pass_pattern,
                            "line_count": line_count,
                        }

                    pass_pattern = checker.find_pass(line)
                    if pass_pattern:
                        matched_pass_pattern = pass_pattern

        if matched_pass_pattern:
            reason = f"timeout reached without fail pattern, pass pattern observed: {matched_pass_pattern}"
        else:
            reason = "timeout reached without fail pattern"

        return {
            "passed": True,
            "reason": reason,
            "fail_pattern": matched_fail_pattern,
            "pass_pattern": matched_pass_pattern,
            "line_count": line_count,
        }
