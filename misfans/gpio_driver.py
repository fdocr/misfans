"""GPIO driver: simple adapter with Fake fallback."""
try:
    from gpiozero import DigitalOutputDevice
except Exception:  # pragma: no cover
    DigitalOutputDevice = None


class FanDriver:
    """Minimal fan driver with on/off/is_active."""

    def __init__(self, pin: int):
        self.pin = int(pin)
        if DigitalOutputDevice is not None:
            self.dev = DigitalOutputDevice(self.pin)
        else:
            self.dev = None

    def on(self) -> None:
        if self.dev:
            self.dev.on()
        else:
            print(f"[fake-gpio] fan ON (pin {self.pin})")

    def off(self) -> None:
        if self.dev:
            self.dev.off()
        else:
            print(f"[fake-gpio] fan OFF (pin {self.pin})")

    def is_active(self) -> bool:
        if self.dev:
            return bool(self.dev.value)
        return False
