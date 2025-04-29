# 🌫️ Raspberry Pi Automated Mushroom Farm – Humidifier Control

This project automates humidity control using a Raspberry Pi and Zigbee sensors for use in mushroom cultivation. It ensures the air stays sufficiently humid by activating a connected humidifier through an Energenie ENER002-2PI smart plug.

---

## 📍 Repository

**GitHub:** [Raspberry-PI-Automated-Mushroom-Farm](https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git)

---

## 📦 Project Contents

| File/Folder               | Description |
|---------------------------|-------------|
| `humidifier_automation.py` | Main automation script that controls the humidifier based on sensor data. |
| `simulate_state_json.py`  | Optional script to generate fake sensor data for testing. |
| `state.json`              | Real-time humidity data, typically updated by Zigbee2MQTT. |
| `state_json_guide.md`     | Describes the structure and purpose of the `state.json` file. |
| `README.md`               | This project overview and setup guide. |

---

## 🛠️ Requirements

- **Hardware:**
  - Raspberry Pi (with GPIO access)
  - Humidifier controlled via Energenie ENER002-2PI smart plug
  - One or more Zigbee humidity sensors
- **Software:**
  - Python 3
  - [Zigbee2MQTT](https://www.zigbee2mqtt.io/)
  - `RPi.GPIO` Python library
  - Linux (tested on Raspberry Pi OS)

---

## ⚙️ Setup Instructions

### 1. Install Required Packages
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install RPi.GPIO
```

### 2. Connect GPIO Pins
Ensure your Energenie ENER002-2PI is wired as per documentation. Default pin mappings:
- Pins 11, 13, 15, 16, 18, and 22 are used.

### 3. Set Up Zigbee2MQTT
- Install and configure Zigbee2MQTT to write humidity data to:
  ```
  /opt/zigbee2mqtt/data/state.json
  ```
- Match sensor names (`sensor1`, `sensor2`) in the script with your actual device IDs.

### 4. Test the System
Run the automation script:
```bash
sudo python3 humidifier_automation.py
```

---

## 🧪 Testing Without Sensors

Use the simulator to generate fake sensor data:
```bash
python3 simulate_state_json.py
```
This will update `state.json` every 60 seconds with realistic values, so you can safely test the system logic.

---

## 🔄 Auto-Start on Boot (Optional)

Create a systemd service to run the automation on startup:

```bash
sudo nano /etc/systemd/system/humidifier.service
```

Paste:
```ini
[Unit]
Description=Humidifier Automation
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/humidifier_automation.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Then enable the service:
```bash
sudo systemctl daemon-reexec
sudo systemctl enable humidifier.service
sudo systemctl start humidifier.service
```

---

## 🧠 Tips & Considerations

- Rebooting every 30 cycles is a precaution for SD card health. Adjust or disable as needed.
- Use proper casing or waterproofing if deploying in humid environments.
- Logging is written to `/var/log/humidifier.log` (can be changed in the script).

---

## 🐛 Troubleshooting

- **GPIO errors**: Check pin permissions or run the script with `sudo`.
- **JSON errors**: Ensure `state.json` is valid and not manually edited while in use.
- **No output from sensors**: Check Zigbee2MQTT logs and device connectivity.

---

## 📜 License

MIT License – Use and modify freely.