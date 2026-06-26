from core.scenario import Scenario, ScenarioResult


class BasicPowerCycleScenario(Scenario):
    name = "basic_power_cycle"

    def run_once(self, index):
        off_delay = self.config.get("aging", "power_off_delay_sec", default=5)
        boot_wait = self.config.get("aging", "boot_wait_sec", default=60)

        self.power.power_cycle(
            off_delay_sec=off_delay,
            boot_wait_sec=boot_wait,
        )

        return ScenarioResult.pass_result("power cycle done")
