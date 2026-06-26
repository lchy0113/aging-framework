import argparse
from pathlib import Path

from core.config import Config
from core.aging_runner import AgingRunner
from controllers import create_power_controller
from scenarios.basic_power_cycle import BasicPowerCycleScenario
from scenarios.ilitek_boot import IlitekBootScenario


SCENARIOS = {
    "basic_power_cycle": BasicPowerCycleScenario,
    "ilitek_boot": IlitekBootScenario,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=SCENARIOS.keys())
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = Config(Path(args.config))
    power = create_power_controller(config)

    scenario_cls = SCENARIOS[args.scenario]
    scenario = scenario_cls(config, power)

    runner = AgingRunner(config, scenario)
    runner.run()


if __name__ == "__main__":
    main()
