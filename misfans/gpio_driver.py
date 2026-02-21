"""GPIO driver: simple adapter with Fake fallback."""
try:
    from gpiozero import DigitalOutputDevice
except Exception:  # pragma: no cover
    DigitalOutputDevice = None


class FanDriver:
    """Minimal fan driver with on/off/is_active."""

    def __init__(self, pin: int):
        self.pin = int(pin)
        # Defer creating the real device until first use to avoid gpiozero
        # trying to load a Pi-specific pin factory on CI runners.
        self.dev = None

    def on(self) -> None:
        # Lazy-init the real device if possible
        if self.dev is None and DigitalOutputDevice is not None:
            try:
                self.dev = DigitalOutputDevice(self.pin)
            except Exception:
                self.dev = None

        if self.dev:
            self.dev.on()
        else:
            print(f"[fake-gpio] fan ON (pin {self.pin})")

    def off(self) -> None:
        # Lazy-init the device (same reasoning as on())
        if self.dev is None and DigitalOutputDevice is not None:
            try:
                self.dev = DigitalOutputDevice(self.pin)
            except Exception:
                self.dev = None

        if self.dev:
            self.dev.off()
        else:
            print(f"[fake-gpio] fan OFF (pin {self.pin})")

    def is_active(self) -> bool:
        if self.dev is None and DigitalOutputDevice is not None:
            try:
                self.dev = DigitalOutputDevice(self.pin)
            except Exception:
                self.dev = None

        if self.dev:
            return bool(self.dev.value)
        return False
