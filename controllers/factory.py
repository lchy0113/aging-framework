from smartthings import SmartThingsClient, SmartPlug
from .smartthings_power_controller import SmartThingsPowerController


def create_power_controller(config):
    controller_type = config.get("power", "controller", default="smartthings")

    if controller_type != "smartthings":
        raise ValueError(f"Unsupported power controller: {controller_type}")

    device_name = config.get("power", "device", default="main_plug")

    client = SmartThingsClient(
        config.smartthings_token(),
        ssl_verify=config.ssl_verify(),
        ca_cert=config.ca_cert(),
    )

    plug = SmartPlug(
        client,
        config.device_id(device_name),
        component=config.device_component(device_name),
    )

    return SmartThingsPowerController(plug)
