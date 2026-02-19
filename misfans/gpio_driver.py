try:
    from gpiozero import DigitalOutputDevice
    GPIO_AVAILABLE = True
except Exception:
    GPIO_AVAILABLE = False


class FanDriver:
    def __init__(self, pin):
        self.pin = pin
        if GPIO_AVAILABLE:
            self.dev = DigitalOutputDevice(pin)
        else:
            self.dev = None

    def on(self):
        if self.dev:
            self.dev.on()
        else:
            print(f"[fake-gpio] fan ON (pin {self.pin})")

    def off(self):
        if self.dev:
            self.dev.off()
        else:
            print(f"[fake-gpio] fan OFF (pin {self.pin})")

    def is_active(self):
        if self.dev:
            return self.dev.value == 1
        return False
