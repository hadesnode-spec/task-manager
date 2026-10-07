#!/bin/bash

set -e


PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/taskmanager.service"


if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

if ! command -v systemctl >/dev/null 2>&1; then
    echo "Error: systemctl is not available."
    exit 1
fi

# Check notify-send
if ! command -v notify-send >/dev/null 2>&1; then
    echo "Error: notify-send is not installed."
    echo "Install it using:"
    echo "sudo apt install libnotify-bin"
    exit 1
fi


mkdir -p "$SERVICE_DIR"


cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Task Manager Reminder Service
After=graphical-session.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/reminder.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

echo "Systemd service created."


systemctl --user daemon-reload


systemctl --user enable taskmanager.service

systemctl --user restart taskmanager.service

echo ""
echo "======================================"
echo " Installation completed successfully!"
echo "======================================"

echo ""
echo "Service status:"
systemctl --user --no-pager status taskmanager.service