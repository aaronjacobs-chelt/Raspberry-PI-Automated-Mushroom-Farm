# 🌫️ Raspberry Pi Automated Mushroom Farm

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-green.svg)](https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm)

> **Acknowledgment**: This project was inspired by the original MycoMonitor project. While the original project is no longer maintained, it provided the foundational concepts and ideas for this implementation. We're grateful for their pioneering work in automated mushroom cultivation.

## 📖 Overview

The Raspberry Pi Automated Mushroom Farm is a complete system for automating humidity control in mushroom cultivation environments. It uses a Raspberry Pi to monitor humidity levels via Zigbee sensors and automatically activates a humidifier (connected through an Energenie smart plug) when humidity falls below your specified threshold.

### ✨ Key Features

- **Automated Humidity Control**: Maintains optimal growing conditions (80-95% humidity) without constant monitoring
- **Multi-Sensor Support**: Works with multiple Zigbee humidity sensors for accurate environmental readings
- **Smart Plug Integration**: Controls standard humidifiers through affordable Energenie ENER002-2PI smart plugs
- **Test Mode**: Includes a simulation script for testing without physical hardware
- **Auto-Start Capability**: Can be configured as a system service that runs automatically on boot
- **Comprehensive Logging**: Detailed logging for monitoring system performance and troubleshooting

### 🔌 Technology Stack

- **Hardware**: Raspberry Pi, Zigbee sensors, Energenie ENER002-2PI smart plug
- **Software**: Python, RPi.GPIO, Zigbee2MQTT
- **Communication**: GPIO pins for smart plug control, Zigbee for wireless sensor data

## ⚡ Quick Start

### Prerequisites

- Raspberry Pi (any model with GPIO access)
- Energenie ENER002-2PI smart plug
- One or more Zigbee humidity sensors
- Zigbee coordinator/hub
- Python 3.6+

### Basic Setup

```bash
# Clone repository
git clone https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git
cd Raspberry-PI-Automated-Mushroom-Farm

# Install dependencies
sudo apt update && sudo apt install python3 python3-pip
pip3 install RPi.GPIO

# Run the automation script
sudo python3 humidifier_automation.py
```

For detailed setup instructions, see the [Configuration Guide](docs/Configuration_Guide.md).

## 📚 Documentation

This project includes comprehensive documentation to help you get started and make the most of your automated mushroom farm:

| Document | Description |
|----------|-------------|
| [Configuration Guide](docs/Configuration_Guide.md) | Detailed configuration of sensors, state.json format, and script settings |
| [Troubleshooting Guide](docs/Troubleshooting.md) | Common issues and solutions for system problems |
| [Development Guide](docs/Development.md) | Information for contributors and developers |
| [docs/images/](docs/images/) | Diagrams and visual references |

## 🛠️ Installation

> **Tip**: Before beginning installation, we recommend reviewing the [System Architecture Diagram](docs/images/system_architecture.md) and [GPIO Connection Diagram](docs/images/gpio_connections.md) for a visual understanding of how all components fit together.

### 1. Hardware Setup

Connect your Energenie ENER002-2PI smart plug to the Raspberry Pi GPIO pins:

| Energenie Wire | Raspberry Pi GPIO Pin |
|----------------|----------------------|
| Red            | Pin 11 (CTRL1)       |
| Black          | Pin 13 (OUTLET)      |
| White          | Pin 15 (CTRL2)       |
| Green          | Pin 16 (CTRL3)       |
| Yellow         | Pin 18 (CTRL4)       |
| Blue           | Pin 22 (TRIGGER)     |

### 2. Software Installation

```bash
# Install required packages
sudo apt update
sudo apt install python3 python3-pip git
pip3 install RPi.GPIO

# Clone and set up the repository
git clone https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git
cd Raspberry-PI-Automated-Mushroom-Farm
```

### 3. Set Up Zigbee2MQTT

Ensure Zigbee2MQTT is configured to write sensor data to a `state.json` file. For detailed instructions, see the [Configuration Guide](docs/Configuration_Guide.md).

### 4. Auto-Start Configuration (Optional)

Set up as a systemd service to run on boot:

```bash
sudo nano /etc/systemd/system/humidifier.service
```

```ini
[Unit]
Description=Mushroom Farm Humidity Automation
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Raspberry-PI-Automated-Mushroom-Farm/humidifier_automation.py
WorkingDirectory=/home/pi/Raspberry-PI-Automated-Mushroom-Farm
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable humidifier.service
sudo systemctl start humidifier.service
```

## 💻 Usage

### Basic Operation

Once installed and configured, the system will:

1. Read humidity data from your Zigbee sensors via the `state.json` file
2. Compare current humidity levels against your configured threshold (default: 95%)
3. Activate the humidifier when humidity falls below the threshold
4. Deactivate the humidifier when humidity reaches satisfactory levels
5. Log all activities to `/var/log/humidifier.log`

### Testing Mode

For testing without physical sensors:

```bash
python3 simulate_state_json.py
```

This will generate simulated sensor data, allowing you to test the system's logic without actual hardware.

### Monitoring

Check the log file for system activity:

```bash
cat /var/log/humidifier.log
```

## ⚙️ Configuration

The main configuration options are found in `humidifier_automation.py`:

```python
# User configurable settings
HUMIDITY_THRESHOLD = 95.0  # Activate humidifier when humidity falls below this value
SENSOR_NAMES = ["sensor1", "sensor2"]  # Names of your Zigbee sensors in state.json
STATE_FILE_PATH = "/opt/zigbee2mqtt/data/state.json"  # Path to your state.json file
LOG_FILE = "/var/log/humidifier.log"  # Path for log file
REBOOT_AFTER_CYCLES = 30  # Reboot after this many cycles (set to 0 to disable)
```

For detailed configuration information, see the [Configuration Guide](docs/Configuration_Guide.md).

## 🤝 Contributing

We welcome contributions to improve this project! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit with clear messages (`git commit -m 'Add feature: description'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

See the [Development Guide](docs/Development.md) for coding standards and development workflow details.

## 📜 License

MIT License – Use and modify freely.

---

<div align="center">
  <p>
    <em>Made with ❤️ for mushroom growers everywhere</em>
  </p>
  <p>
    <a href="https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm/issues">Report Bug</a> •
    <a href="https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm/issues">Request Feature</a>
  </p>
</div>
