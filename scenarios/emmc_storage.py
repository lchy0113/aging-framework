import subprocess
import time
from datetime import datetime

from core.scenario import Scenario, ScenarioResult
from core.logger import make_log_path


class EmmcStorageScenario(Scenario):
    name = "emmc_storage"

    def adb_shell(self, cmd, timeout=30):
        result = subprocess.run(
            ["adb", "shell", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def wait_boot_completed(self, timeout_sec):
        start = time.time()

        while time.time() - start < timeout_sec:
            rc, out, _ = self.adb_shell("getprop sys.boot_completed", timeout=10)
            if rc == 0 and out.strip() == "1":
                return True

            time.sleep(3)

        return False

    def collect_emmc_info(self, device_node):
        commands = [
            f"cat /sys/block/{device_node}/device/name",
            f"cat /sys/block/{device_node}/device/cid",
            f"cat /sys/block/{device_node}/device/csd",
            f"cat /sys/block/{device_node}/device/type",
            f"cat /sys/block/{device_node}/size",
            f"cat /sys/block/{device_node}/device/life_time 2>/dev/null",
            f"cat /sys/block/{device_node}/device/pre_eol_info 2>/dev/null",
            "cat /sys/kernel/debug/mmc2/ios 2>/dev/null",
            "cat /proc/partitions",
        ]

        output = []

        for cmd in commands:
            rc, out, err = self.adb_shell(cmd)
            output.append(f"$ {cmd}")
            output.append(out if rc == 0 else err)
            output.append("")

        return "\n".join(output)

    def write_verify(self, test_size_mb):
        test_file = "/data/local/tmp/emmc_test.bin"

        self.adb_shell(f"rm -f {test_file}")

        rc, out, err = self.adb_shell(
            f"dd if=/dev/zero of={test_file} bs=1M count={test_size_mb} conv=fsync",
            timeout=300,
        )
        if rc != 0:
            return False, "WRITE_FAIL", err or out

        self.adb_shell("sync", timeout=60)

        rc, hash1, err = self.adb_shell(f"sha256sum {test_file} | awk '{{print $1}}'")
        if rc != 0 or not hash1:
            return False, "HASH_CREATE_FAIL", err

        rc, hash2, err = self.adb_shell(f"sha256sum {test_file} | awk '{{print $1}}'")
        if rc != 0 or not hash2:
            return False, "HASH_VERIFY_FAIL", err

        self.adb_shell(f"rm -f {test_file}")
        self.adb_shell("sync", timeout=60)

        if hash1 != hash2:
            return False, "HASH_MISMATCH", f"{hash1} != {hash2}"

        return True, "WRITE_VERIFY_PASS", hash1

    def scan_error_log(self):
        pattern = (
            "mmc.*timeout|"
            "mmc.*CRC|"
            "mmc.*I/O error|"
            "Buffer I/O error|"
            "blk_update_request.*I/O error|"
            "end_request.*I/O error|"
            "EXT4-fs error|"
            "F2FS-fs error|"
            "Unable to mount|"
            "mount failed|"
            "Kernel panic|"
            "panic|"
            "rpmb.*fail"
        )

        exclude = (
            "ReadFstabFromDt\\(\\): failed to read fstab from dt|"
            "EXT4-fs \\(.*\\): mounted filesystem|"
            "EXT4-fs \\(.*\\): recovery complete"
        )

        cmd = f"dmesg | grep -Ei '{pattern}' | grep -Eiv '{exclude}'"

        rc, out, _ = self.adb_shell(cmd, timeout=30)

        if out:
            return False, out

        return True, ""

    def run_once(self, index):
        start_dt = datetime.now()
        start_time = start_dt.strftime("%Y-%m-%d %H:%M:%S")

        device_node = self.config.get("emmc", "device_node", default="mmcblk2")
        test_size_mb = self.config.get("emmc", "test_size_mb", default=128)
        boot_timeout = self.config.get("emmc", "boot_timeout_sec", default=180)
        off_delay = self.config.get("aging", "power_off_delay_sec", default=5)

        print(f"[{index:04d}] Power OFF")
        self.power.power_off()
        time.sleep(off_delay)

        print(f"[{index:04d}] Power ON")
        self.power.power_on()

        print(f"[{index:04d}] Wait Android boot complete")
        boot_ok = self.wait_boot_completed(boot_timeout)

        log_path = make_log_path("raw", "emmc", index)

        if not boot_ok:
            end_dt = datetime.now()
            return ScenarioResult.fail_result(
                "BOOT_TIMEOUT",
                str(log_path),
                start_time=start_time,
                end_time=end_dt.strftime("%Y-%m-%d %H:%M:%S"),
                duration_sec=round((end_dt - start_dt).total_seconds(), 3),
            )

        emmc_info = self.collect_emmc_info(device_node)
        rw_ok, rw_reason, rw_detail = self.write_verify(test_size_mb)
        log_ok, fail_log = self.scan_error_log()

        end_dt = datetime.now()
        end_time = end_dt.strftime("%Y-%m-%d %H:%M:%S")
        duration_sec = round((end_dt - start_dt).total_seconds(), 3)

        log_path.write_text(
            "\n".join([
                "===== eMMC INFO =====",
                emmc_info,
                "===== WRITE VERIFY =====",
                rw_reason,
                rw_detail,
                "===== ERROR LOG =====",
                fail_log,
            ]),
            encoding="utf-8",
        )

        if not rw_ok:
            return ScenarioResult.fail_result(
                rw_reason,
                str(log_path),
                fail_pattern=rw_reason,
                start_time=start_time,
                end_time=end_time,
                duration_sec=duration_sec,
            )

        if not log_ok:
            return ScenarioResult.fail_result(
                "KERNEL_STORAGE_ERROR",
                str(log_path),
                fail_pattern=fail_log[:120],
                start_time=start_time,
                end_time=end_time,
                duration_sec=duration_sec,
            )

        return ScenarioResult.pass_result(
            rw_reason,
            str(log_path),
            start_time=start_time,
            end_time=end_time,
            duration_sec=duration_sec,
        )