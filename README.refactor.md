Refactor -> misfans (Python)

This refactor replaces the original Ruby scripts with a Python 3 service.

Usage (after installation):
- Configure /etc/misfans.env or export env vars: FAN_PIN, ON_TEMP, OFF_TEMP, POLL_INTERVAL
- Install systemd unit (provided in systemd/misfans.service)
- Enable and start: sudo systemctl daemon-reload && sudo systemctl enable --now misfans.service

Defaults:
- FAN_PIN=4
- ON_TEMP=55
- OFF_TEMP=50
- POLL_INTERVAL=5

Details and developer notes in the PR.
