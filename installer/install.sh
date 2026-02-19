#!/usr/bin/env bash
set -euo pipefail

# Installer script for misfans
# Usage: sudo ./install.sh

SERVICE_NAME=misfans
ENV_FILE=/etc/misfans.env
SERVICE_FILE=/etc/systemd/system/misfans.service
USER_NAME=misfans
GROUP_NAME=gpio

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

echo "Creating user $USER_NAME (if not exists)"
if ! id -u $USER_NAME >/dev/null 2>&1; then
  useradd --system --home /var/lib/misfans --shell /usr/sbin/nologin $USER_NAME
fi

# Add to gpio group if exists
if getent group $GROUP_NAME >/dev/null 2>&1; then
  usermod -aG $GROUP_NAME $USER_NAME || true
fi

# Copy environment example if not present
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<EOF
FAN_PIN=4
POLL_INTERVAL=5
ON_TEMP=55
OFF_TEMP=50
EOF
  chmod 640 "$ENV_FILE"
fi

# Install systemd unit
SCRIPT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cp "$SCRIPT_DIR/systemd/misfans.service" "$SERVICE_FILE"
chown root:root "$SERVICE_FILE"
chmod 644 "$SERVICE_FILE"

systemctl daemon-reload
systemctl enable --now $SERVICE_NAME.service

echo "Installed and started $SERVICE_NAME.service"
