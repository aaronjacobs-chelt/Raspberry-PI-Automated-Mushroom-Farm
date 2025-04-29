import json
import random
import time

# Configuration
output_file = "state.json"
sensors = ["sensor1", "sensor2"]
humidity_range = (85.0, 99.0)
temperature_range = (18.0, 24.0)
battery_range = (90, 100)
linkquality_range = (100, 160)
update_interval = 60  # seconds

def generate_sensor_data():
    return {
        "humidity": round(random.uniform(*humidity_range), 1),
        "temperature": round(random.uniform(*temperature_range), 1),
        "battery": random.randint(*battery_range),
        "linkquality": random.randint(*linkquality_range)
    }

def simulate():
    while True:
        data = {sensor: generate_sensor_data() for sensor in sensors}
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Updated {output_file} with simulated sensor data.")
        time.sleep(update_interval)

if __name__ == "__main__":
    simulate()
