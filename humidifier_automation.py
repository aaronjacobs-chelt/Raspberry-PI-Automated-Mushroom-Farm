import os
import time
import json
import logging
import RPi.GPIO as GPIO
from datetime import datetime

# === Configuration ===
SENSOR_FILE = "/opt/zigbee2mqtt/data/state.json"
HUMIDITY_THRESHOLD = 95.0
ACTIVATION_TIME = 30
CYCLE_REBOOT_LIMIT = 30
STALE_DATA_THRESHOLD = 30  # Number of unchanged reads before forced humidification
SENSOR_NAMES = ["sensor1", "sensor2"]  # Update as needed

GPIO_PINS = {
    "OUTLET": 13,
    "CTRL1": 11,
    "CTRL2": 15,
    "CTRL3": 16,
    "CTRL4": 18,
    "TRIGGER": 22,
}

# === Logging Setup ===
logging.basicConfig(
    filename='/var/log/humidifier.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# === Controller Class ===
class HumidifierController:
    def __init__(self):
        self.reboot_counter = 0
        self.dry_counter = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        for pin in GPIO_PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        logging.info("GPIO setup complete.")

    def cleanup_and_reboot(self):
        logging.info("Cleaning up GPIO and rebooting system.")
        self.turn_off()
        GPIO.cleanup()
        os.system("sudo reboot")

    def send_signal(self, pins, delay1=0.1, delay2=0.25):
        for pin in pins:
            GPIO.output(pin, True)
        time.sleep(delay1)
        GPIO.output(GPIO_PINS["TRIGGER"], True)
        time.sleep(delay2)
        GPIO.output(GPIO_PINS["TRIGGER"], False)

    def on(self):
        self.send_signal([GPIO_PINS["CTRL1"], GPIO_PINS["CTRL2"], GPIO_PINS["CTRL3"], GPIO_PINS["OUTLET"]])
        logging.info("Humidifier ON signal sent.")

    def off(self):
        self.send_signal([GPIO_PINS["CTRL1"], GPIO_PINS["CTRL2"], GPIO_PINS["CTRL3"]], delay1=0.1)
        GPIO.output(GPIO_PINS["OUTLET"], False)
        time.sleep(0.25)
        logging.info("Humidifier OFF signal sent.")

    def turn_on(self):
        self.on()
        while GPIO.input(GPIO_PINS["OUTLET"]) is not True:
            logging.warning("Retrying humidifier ON...")
            time.sleep(5)
            self.on()

    def turn_off(self):
        self.off()
        while GPIO.input(GPIO_PINS["OUTLET"]) is not False:
            logging.warning("Retrying humidifier OFF...")
            self.on()
            time.sleep(5)
            self.off()

    def read_humidity(self, sensor):
        try:
            with open(SENSOR_FILE) as f:
                data = json.load(f)
            humidity = float(data[sensor]["humidity"])
            return humidity
        except Exception as e:
            logging.error(f"Failed to read sensor '{sensor}': {e}")
            return None

    def run(self):
        try:
            while self.reboot_counter <= CYCLE_REBOOT_LIMIT:
                readings = [self.read_humidity(s) for s in SENSOR_NAMES]
                if any(h is not None and h < HUMIDITY_THRESHOLD for h in readings):
                    logging.info(f"Low humidity detected: {readings}")
                    for _ in range(3):
                        self.turn_on()
                        time.sleep(ACTIVATION_TIME)
                        self.turn_off()
                        time.sleep(60)
                    time.sleep(180)
                else:
                    logging.info(f"Humidity OK: {readings}")
                self.reboot_counter += 1

                # Wait for fresh readings
                prev_readings = readings
                while True:
                    time.sleep(120)
                    new_readings = [self.read_humidity(s) for s in SENSOR_NAMES]
                    if new_readings != prev_readings:
                        self.dry_counter = 0
                        break
                    self.dry_counter += 1
                    logging.warning(f"No new sensor data for {self.dry_counter * 2} minutes.")
                    if self.dry_counter >= STALE_DATA_THRESHOLD:
                        logging.warning("Stale data threshold reached — activating humidifier as fallback.")
                        self.turn_on()
                        time.sleep(ACTIVATION_TIME)
                        self.turn_off()
                        self.dry_counter = 0
                        break
        finally:
            self.cleanup_and_reboot()

# === Main ===
if __name__ == "__main__":
    controller = HumidifierController()
    controller.run()
