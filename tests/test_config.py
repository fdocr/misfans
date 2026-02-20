from misfans.config import Config

def test_config_defaults(monkeypatch):
    monkeypatch.delenv('FAN_PIN', raising=False)
    monkeypatch.delenv('POLL_INTERVAL', raising=False)
    monkeypatch.delenv('ON_TEMP', raising=False)
    monkeypatch.delenv('OFF_TEMP', raising=False)
    c = Config()
    assert c.FAN_PIN == 4
    assert c.POLL_INTERVAL == 5.0
    assert c.ON_TEMP == 55.0
    assert c.OFF_TEMP == 50.0
