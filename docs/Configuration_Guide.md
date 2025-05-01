# 📝 Configuration Guide

This guide explains the configuration options and file formats used in the Raspberry Pi Automated Mushroom Farm system.

## 🔧 System Configuration

The system uses two main configuration mechanisms:
1. Environment variables or command-line arguments for basic settings
2. The `state.json` file for real-time sensor data

## 📊 state.json Format

The `state.json` file is used by the humidifier automation script to determine when to activate or deactivate the humidifier. This file is expected to be automatically updated by Zigbee2MQTT and should contain structured data for each Zigbee humidity sensor.

### Example Structure:
```json
{
  "sensor1": {
    "humidity": 92.3,
    "temperature": 20.5,
    "battery": 97,
    "linkquality": 150
  },
  "sensor2": {
    "humidity": 94.7,
    "temperature": 21.1,
    "battery": 95,
    "linkquality": 144
  }
}
```

### Field Descriptions:

| Field         | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| `humidity`    | Float   | Relative humidity percentage. This is the key value used by the automation script to decide whether to turn the humidifier on or off. |
| `temperature` | Float   | Temperature in degrees Celsius. This value is optional and not used by the script. |
| `battery`     | Integer | Sensor battery level as a percentage. Optional, for reference.              |
| `linkquality` | Integer | Zigbee signal strength. Higher values indicate better connection quality.   |

### Important Notes:
- Sensor keys like `"sensor1"` or `"sensor2"` must match those defined in the Python script (`SENSOR_NAMES` list).
- Only the `humidity` field is used by the automation script.
- The file should be in valid JSON format (no comments) to be parsed correctly by the script.

## ⚙️ Script Configuration

The main script `humidifier_automation.py` includes several configurable parameters:

```python
# User configurable settings
HUMIDITY_THRESHOLD = 95.0  # Activate humidifier when humidity falls below this value
SENSOR_NAMES = ["sensor1", "sensor2"]  # Names of your Zigbee sensors in state.json
STATE_FILE_PATH = "/opt/zigbee2mqtt/data/state.json"  # Path to your state.json file
LOG_FILE = "/var/log/humidifier.log"  # Path for log file
REBOOT_AFTER_CYCLES = 30  # Reboot after this many cycles (set to 0 to disable)
```

You should modify these values to match your specific setup before running the script.

## 🌐 Zigbee2MQTT Configuration

To integrate with this system, your Zigbee2MQTT configuration should:

1. Enable MQTT state publishing
2. Configure the correct output path for `state.json`

Example Zigbee2MQTT configuration:

```yaml
# Configuration for Zigbee2MQTT
homeassistant: false
permit_join: false
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://localhost:1883
serial:
  port: /dev/ttyACM0
devices:
  '0x00158d0001d82999':
    friendly_name: 'sensor1'
  '0x00158d0001d83000':
    friendly_name: 'sensor2'
advanced:
  log_level: info
  log_output:
    - console
  # This enables saving state to state.json
  state_path: /opt/zigbee2mqtt/data/state.json
  state_debounce: 0.5
```

## 🔌 Hardware Connections

The proper hardware setup is critical for system functionality. The Raspberry Pi connects to the Energenie ENER002-2PI controller through specific GPIO pins as follows:

| Wire Color | Raspberry Pi GPIO Pin | Function |
|------------|----------------------|----------|
| RED        | Pin 11               | CTRL1    |
| BLACK      | Pin 13               | OUTLET   |
| WHITE      | Pin 15               | CTRL2    |
| GREEN      | Pin 16               | CTRL3    |
| YELLOW     | Pin 18               | CTRL4    |
| BLUE       | Pin 22               | TRIGGER  |

For a complete visual guide with connection diagrams, see the [GPIO Connection Diagram](images/gpio_connections.md).
