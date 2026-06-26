from .power_controller import PowerController


class SmartThingsPowerController(PowerController):
    def __init__(self, plug):
        self.plug = plug

    def power_on(self):
        return self.plug.on()

    def power_off(self):
        return self.plug.off()
