from abc import ABC, abstractmethod
import time


class PowerController(ABC):
    @abstractmethod
    def power_on(self):
        pass

    @abstractmethod
    def power_off(self):
        pass

    def power_cycle(self, off_delay_sec=5, boot_wait_sec=60):
        print("[PowerController] OFF")
        self.power_off()
        time.sleep(off_delay_sec)

        print("[PowerController] ON")
        self.power_on()
        time.sleep(boot_wait_sec)
