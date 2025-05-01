# MycoMonitor Quick Start Guide

## 1. Hardware Setup

1. **Connect Energenie Smart Plug**:
   ```
   GPIO Connections:
   - Red -> Pin 11 (CTRL1)
   - Black -> Pin 13 (OUTLET)
   - White -> Pin 15 (CTRL2)
   - Green -> Pin 16 (CTRL3)
   - Yellow -> Pin 18 (CTRL4)
   - Blue -> Pin 22 (TRIGGER)
   ```

2. **Connect Zigbee Coordinator**:
   - Plug into USB port
   - Note device path (usually /dev/ttyACM0)

3. **Setup Sensors**:
   - Place primary sensor at mushroom height
   - Place secondary sensor for gradient monitoring
   - Ensure good air circulation around sensors

## 2. Quick Installation

```bash
# Clone repository
git clone https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git
cd Raspberry-PI-Automated-Mushroom-Farm

# Run installer
./scripts/deploy.sh
```

## 3. Basic Configuration

1. **Edit config**:
   ```bash
   sudo nano /etc/mycomonitor/mycomonitor.json
   ```

2. **Set sensor names**:
   ```json
   {
     "sensor_names": ["mushroom_height", "upper_shelf"],
     "humidity_threshold": 95.0
   }
   ```

## 4. Start System

```bash
sudo systemctl start mycomonitor
sudo systemctl start mycomonitor-web
```

## 5. Monitor

1. **Check status**:
   ```bash
   mycomonitor status
   ```

2. **View web dashboard**:
   ```
   http://your-pi-ip:8080
   ```

3. **Watch logs**:
   ```bash
   tail -f /var/log/mycomonitor/mycomonitor.log
   ```

## Need Help?

- Check [Installation Guide](../INSTALL.md)
- See [Troubleshooting](troubleshooting.md)
- Open an [Issue](https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm/issues)

