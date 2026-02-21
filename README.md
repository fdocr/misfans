# misfans — Raspberry Pi fan controller

misfans is a small Python 3 package that runs as a systemd-friendly daemon to control a Raspberry Pi fan based on temperature.

## Quick start

1. On the target Pi, ensure Python 3.10+ is installed.
2. Clone this repo:

   `git clone https://github.com/fdocr/misfans.git && cd misfans`


3. Run the installer as root (creates `misfans` user and service):

   `sudo ./installer/install.sh`
4. Edit `/etc/misfans.env` to tune thresholds and pin numbers, then restart the service:

   `sudo systemctl restart misfans.service`

## Configuration

The installer creates `/etc/misfans.env` with sensible defaults:

```
FAN_PIN=4
POLL_INTERVAL=5
ON_TEMP=60
OFF_TEMP=50
```

Change values as needed.

## Development

- Tests: `pytest -q`
- Lint: `ruff check .`
- If you don't have GPIO available, the `gpio_driver` falls back to a fake driver so tests and local runs won't require hardware.

Why Python?

Python is the standard scripting language on Raspberry Pi and many embedded devices. It has excellent library support (gpiozero, dotenv), makes mocking and testing hardware interactions straightforward, and is easy for contributors to read and extend.

License

MIT

## Useful commands

- Install for development (editable): `python -m venv .venv && . .venv/bin/activate && pip install -e . && pip install -r requirements.txt`
- Run daemon in foreground (for debugging): `python -m misfans.daemon`
- Check service status: `sudo systemctl status misfans.service`
- View logs: `sudo journalctl -u misfans.service -f`
- Start/stop service: `sudo systemctl start|stop misfans.service`

License

MIT
