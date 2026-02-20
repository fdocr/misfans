# misfans — Raspberry Pi fan controller

misfans is a small Python 3 package that runs as a systemd-friendly daemon to control a Raspberry Pi fan based on temperature.

Highlights

- Python package `misfans/` with:
  - `daemon.py` — main controller loop
  - `gpio_driver.py` — hardware abstraction + fake fallback for development
  - `config.py` — environment-based configuration
  - `utils.py` — CPU temperature reader
- `systemd/misfans.service` — unit file template (runs as `misfans` user)
- `installer/install.sh` — idempotent install script to create the user, write `/etc/misfans.env`, create a virtualenv, install the package, and enable the service
- `tests/` — pytest unit tests for hysteresis and config parsing
- CI: GitHub Actions workflow runs pytest on push/PR

Quick start

1. On the target Pi, ensure Python 3.10+ is installed.
2. Clone this repo and check out the branch (or after merge):

   git clone https://github.com/fdocr/misfans.git
   cd misfans

3. Run the installer as root (creates `misfans` user and service):

   git clone https://github.com/fdocr/misfans.git\   cd misfans\   sudo ./installer/install.sh
4. Edit `/etc/misfans.env` to tune thresholds and pin numbers, then restart the service:

   sudo systemctl restart misfans.service

Configuration

The installer creates `/etc/misfans.env` with sensible defaults:

```
FAN_PIN=4
POLL_INTERVAL=5
ON_TEMP=55
OFF_TEMP=50
```

Change values as needed.

Development

- Tests: `pytest -q`
- If you don't have GPIO available, the `gpio_driver` falls back to a fake driver so tests and local runs won't require hardware.

Why Python?

Python is the standard scripting language on Raspberry Pi and many embedded devices. It has excellent library support (gpiozero, dotenv), makes mocking and testing hardware interactions straightforward, and is easy for contributors to read and extend.

License

MIT
