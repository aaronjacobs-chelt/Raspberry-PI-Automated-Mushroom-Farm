# MycoMonitor Installation Guide

## Quick Installation

For a standard installation on Raspberry Pi:

```bash
# Clone the repository
git clone https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git
cd Raspberry-PI-Automated-Mushroom-Farm

# Run deployment script
./scripts/deploy.sh
```

## Manual Installation Steps

### 1. System Requirements

- Raspberry Pi (3 or newer recommended)
- Raspberry Pi OS (Bullseye or newer)
- Python 3.9+
- Zigbee2MQTT setup
- Energenie ENER002-2PI smart plug

### 2. Hardware Setup

1. Connect Energenie ENER002-2PI:
   ```
   GPIO Pins:
   - Pin 11 (CTRL1)
   - Pin 13 (OUTLET)
   - Pin 15 (CTRL2)
   - Pin 16 (CTRL3)
   - Pin 18 (CTRL4)
   - Pin 22 (TRIGGER)
   ```

2. Setup Zigbee network:
   - Install Zigbee coordinator
   - Configure sensors
   - Connect humidifier to smart plug

### 3. Software Installation

1. Create installation directories:
   ```bash
   sudo mkdir -p /opt/mycomonitor
   sudo mkdir -p /etc/mycomonitor
   sudo mkdir -p /var/lib/mycomonitor
   sudo mkdir -p /var/log/mycomonitor
   ```

2. Set permissions:
   ```bash
   sudo chown -R pi:pi /opt/mycomonitor
   sudo chown -R pi:pi /etc/mycomonitor
   sudo chown -R pi:pi /var/lib/mycomonitor
   sudo chown -R pi:pi /var/log/mycomonitor
   ```

3. Install Python dependencies:
   ```bash
   python3 -m venv /opt/mycomonitor/venv
   source /opt/mycomonitor/venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

4. Copy configuration files:
   ```bash
   sudo cp examples/config/mycomonitor.json /etc/mycomonitor/
   sudo cp examples/systemd/mycomonitor.service /etc/systemd/system/
   sudo cp examples/logrotate/mycomonitor /etc/logrotate.d/
   ```

### 4. Configuration

1. Edit main configuration:
   ```bash
   sudo nano /etc/mycomonitor/mycomonitor.json
   ```
   
   Update sensor names and thresholds as needed.

2. Setup logging:
   ```bash
   sudo systemctl restart rsyslog
   ```

3. Enable and start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable mycomonitor
   sudo systemctl start mycomonitor
   ```

### 5. Verify Installation

1. Check service status:
   ```bash
   sudo systemctl status mycomonitor
   ```

2. Monitor logs:
   ```bash
   tail -f /var/log/mycomonitor/mycomonitor.log
   ```

3. Test CLI:
   ```bash
   mycomonitor status
   ```

## Web Interface

1. Enable web interface:
   ```bash
   sudo systemctl enable mycomonitor-web
   sudo systemctl start mycomonitor-web
   ```

2. Access dashboard:
   ```
   http://your-pi-ip:8080
   ```

## Backup Setup

1. Configure backup location:
   ```bash
   sudo mkdir -p /var/backups/mycomonitor
   sudo chown pi:pi /var/backups/mycomonitor
   ```

2. Setup backup script:
   ```bash
   sudo cp scripts/backup.sh /opt/mycomonitor/
   sudo chmod +x /opt/mycomonitor/backup.sh
   ```

3. Add to crontab:
   ```bash
   (crontab -l 2>/dev/null; echo "0 2 * * * /opt/mycomonitor/backup.sh") | crontab -
   ```

## Troubleshooting

### Common Issues

1. Permission Errors:
   ```bash
   sudo chown -R pi:pi /opt/mycomonitor
   sudo chmod -R 755 /opt/mycomonitor
   ```

2. GPIO Access:
   ```bash
   sudo usermod -a -G gpio pi
   ```

3. Service Won't Start:
   ```bash
   sudo journalctl -u mycomonitor -n 50
   ```

### Support

For additional help:
- Check logs: `/var/log/mycomonitor/`
- GitHub Issues: [Project Issues](https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm/issues)
- Email: git@happycaps.co.uk

## Maintenance

### Regular Tasks

1. Check logs daily:
   ```bash
   tail -n 100 /var/log/mycomonitor/mycomonitor.log
   ```

2. Verify backups:
   ```bash
   ls -l /var/backups/mycomonitor/
   ```

3. Update system:
   ```bash
   sudo apt update && sudo apt upgrade
   pip install --upgrade mycomonitor
   ```

### Monitoring

1. Check system status:
   ```bash
   mycomonitor status
   ```

2. View metrics:
   ```bash
   mycomonitor metrics --hours 24
   ```

3. Run diagnostics:
   ```bash
   mycomonitor diagnose
   ```

---

For more detailed information, see the [full documentation](docs/README.md).
