#!/usr/bin/env bash
set -euo pipefail

# Installer script for misfans
# Usage: sudo ./install.sh

SERVICE_NAME=misfans
ENV_FILE=/etc/misfans.env
SERVICE_FILE=/etc/systemd/system/misfans.service
USER_NAME=misfans
GROUP_NAME=gpio
INSTALL_PREFIX=/opt/misfans
VENV_DIR="$INSTALL_PREFIX/venv"

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

# Create install prefix
mkdir -p "$INSTALL_PREFIX"
chown $USER_NAME:$USER_NAME "$INSTALL_PREFIX" || true

# Create virtualenv and install package
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
# Upgrade pip and install
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install "$PWD"[all] || "$VENV_DIR/bin/pip" install -r "$PWD/requirements.txt"

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

# Install systemd unit (adjust ExecStart to venv python)
SCRIPT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cp "$SCRIPT_DIR/systemd/misfans.service" "$SERVICE_FILE"
# Substitute python path in service
sed -i "s|ExecStart=.*|ExecStart=$VENV_DIR/bin/python -m misfans.daemon|" "$SERVICE_FILE"
chown root:root "$SERVICE_FILE"
chmod 644 "$SERVICE_FILE"

systemctl daemon-reload
systemctl enable --now $SERVICE_NAME.service

echo "Installed and started $SERVICE_NAME.service"
