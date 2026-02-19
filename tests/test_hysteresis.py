import tempfile
from misfans.daemon import FanController
from misfans.gpio_driver import FanDriver
from misfans import config

class FakeFan:
    def __init__(self):
        self._state = False
    def on(self):
        self._state = True
    def off(self):
        self._state = False
    def is_active(self):
        return self._state

def test_hysteresis_behavior(monkeypatch):
    c = FanController()
    # replace real fan with fake
    fake = FakeFan()
    fake.off()
    c.fan = fake
    c.on_temp = 60
    c.off_temp = 55

    # below off_temp -> fan stays off
    import misfans.daemon as md
    monkeypatch.setattr(md, 'read_cpu_temp_c', lambda: 50)
    c.check_once()
    assert not fake.is_active()

    # go above on_temp -> fan turns on
    import misfans.daemon as md
    monkeypatch.setattr(md, 'read_cpu_temp_c', lambda: 61)
    c.check_once()
    assert fake.is_active()

    # drop but still above off_temp -> stays on
    import misfans.daemon as md
    monkeypatch.setattr(md, 'read_cpu_temp_c', lambda: 56)
    c.check_once()
    assert fake.is_active()

    # drop below off_temp -> turns off
    import misfans.daemon as md
    monkeypatch.setattr(md, 'read_cpu_temp_c', lambda: 54)
    c.check_once()
    assert not fake.is_active()
