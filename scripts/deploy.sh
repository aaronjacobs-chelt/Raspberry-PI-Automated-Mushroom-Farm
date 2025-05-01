#!/bin/bash

# MycoMonitor Deployment Script

set -e

# Load configuration
CONFIG_FILE="examples/config/deployment.yml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Deployment configuration not found: $CONFIG_FILE"
    exit 1
fi

# Create required directories
sudo mkdir -p /opt/mycomonitor
sudo mkdir -p /etc/mycomonitor
sudo mkdir -p /var/lib/mycomonitor
sudo mkdir -p /var/log/mycomonitor
sudo mkdir -p /var/backups/mycomonitor

# Set permissions
sudo chown -R pi:pi /opt/mycomonitor
sudo chown -R pi:pi /etc/mycomonitor
sudo chown -R pi:pi /var/lib/mycomonitor
sudo chown -R pi:pi /var/log/mycomonitor
sudo chown -R pi:pi /var/backups/mycomonitor

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git

# Create virtual environment
python3 -m venv /opt/mycomonitor/venv
source /opt/mycomonitor/venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install MycoMonitor
pip install -e .

# Copy configuration
sudo cp examples/config/mycomonitor.json /etc/mycomonitor/
sudo cp examples/systemd/mycomonitor.service /etc/systemd/system/
sudo cp examples/logrotate/mycomonitor /etc/logrotate.d/

# Setup logging
sudo systemctl daemon-reload
sudo systemctl enable mycomonitor
sudo systemctl start mycomonitor

# Setup backup script
sudo cp scripts/backup.sh /opt/mycomonitor/
sudo chmod +x /opt/mycomonitor/backup.sh

# Add backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/mycomonitor/backup.sh") | crontab -

echo "MycoMonitor deployment completed"
