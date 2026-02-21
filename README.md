# misfans — Raspberry Pi fan controller

misfans is a small Python 3 package that runs as a systemd-friendly daemon to control a Raspberry Pi fan based on temperature.

## Quick start

Fan wiring differs based on which fan you own, so everyone's setup might be a little different. The default fan pin will be high (ON) when the fan needs to be running, and it will be low (OFF) when it doesn't. This project uses FAN_PIN=4 and refers to BCM GPIO 4 (this is physical pin 7) on common Raspberry Pi's layouts. Keep in mind you can update which pin you use for enabling your fan (you might need 5V so other components might be required). Feel free to create an issue if you need help or have a question on your specific setup.

1. On the target Pi, ensure Python 3.10+ is installed.
2. Clone this repo:

   `git clone https://github.com/fdocr/misfans.git && cd misfans`

3. Run the installer as root (creates `misfans` user and service):

   `sudo bin/install-misfans`

5. Edit `/etc/misfans.env` to tune thresholds and pin numbers, then restart the service:

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



## Update an existing installation

If you already have a clone of this repository and installed the service previously, update your installation with these commands (replace /path/to/your/local/clone with the path to your checked‑out copy):

```
cd /path/to/your/local/clone
git pull --ff-only
sudo ./bin/install-misfans
sudo systemctl restart misfans.service
```

This pulls the latest code into your local clone, runs the installer to install into /opt/misfans/venv (non-editable), and restarts the systemd service.

## Useful commands

`python -m misfans.daemon` — Run the daemon in the foreground (debugging)

`sudo systemctl status misfans.service` — Check the service status

`sudo journalctl -u misfans.service -f` — Follow the service logs

`sudo systemctl start misfans.service` — Start the service

`sudo systemctl stop misfans.service` — Stop the service

`sudo ./bin/install-misfans --uninstall` — Uninstall the service and remove /opt/misfans (run from the installer clone or give full path)

## License

MIT
