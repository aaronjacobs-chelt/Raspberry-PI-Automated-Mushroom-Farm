### `state.json` Format Guide

The `state.json` file is used by the humidifier automation script to determine when to activate or deactivate the humidifier. This file is expected to be automatically updated by Zigbee2MQTT and should contain structured data for each Zigbee humidity sensor.

---

### 📦 Example Structure:
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

---

### 📝 Field Descriptions:

| Field         | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| `humidity`    | Float   | Relative humidity percentage. This is the key value used by the automation script to decide whether to turn the humidifier on or off. |
| `temperature` | Float   | Temperature in degrees Celsius. This value is optional and not used by the script. |
| `battery`     | Integer | Sensor battery level as a percentage. Optional, for reference.              |
| `linkquality` | Integer | Zigbee signal strength. Higher values indicate better connection quality.   |

---

### 🔖 Notes:
- Sensor keys like `"sensor1"` or `"sensor2"` must match those defined in the Python script (`SENSOR_NAMES` list).
- Only the `humidity` field is used by the automation script.
- The file should be in valid JSON format (no comments) to be parsed correctly by the script.
- You can keep a commented version (e.g. `state_example.jsonc`) for reference if needed.

---

