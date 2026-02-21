# misfans — Raspberry Pi fan controller

misfans is a small Python 3 package that runs as a systemd-friendly daemon to control a Raspberry Pi fan based on temperature.

## Quick start

Before you start: wiring the fan

- The fan has two wires: red (live) and black (ground). Connect the black wire to a Raspberry Pi ground pin (GND). Connect the red wire to the GPIO pin you configured for FAN_PIN through a suitable transistor or MOSFET and flyback diode (do not connect the fan directly to a GPIO pin — use a proper low-side switch and separate 5V/3.3V power as required by your fan). If you're unsure, use a GPIO-capable relay board or an appropriate driver module. Double-check polarity and connections before powering the Pi.

1. On the target Pi, ensure Python 3.10+ is installed.
2. Clone this repo:

   `git clone https://github.com/fdocr/misfans.git && cd misfans`


3. Run the installer as root (creates `misfans` user and service):

   `sudo ./installer/install.sh`
4. Edit `/etc/misfans.env` to tune thresholds and pin numbers, then restart the service:

   `sudo systemctl.restart misfans.service`

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



## Useful commands

`python -m misfans.daemon` — Run the daemon in the foreground (debugging)

`sudo systemctl status misfans.service` — Check the service status

`sudo journalctl -u misfans.service -f` — Follow the service logs

`sudo systemctl start misfans.service` — Start the service

`sudo systemctl stop misfans.service` — Stop the service

## License

MIT
