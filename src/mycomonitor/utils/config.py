"""Configuration management for MycoMonitor."""

import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "humidity_threshold": 95.0,
    "activation_time": 30,
    "cycle_reboot_limit": 30,
    "stale_data_threshold": 30,
    "sensor_names": ["sensor1", "sensor2"],
    "gpio_pins": {
        "OUTLET": 13,
        "CTRL1": 11,
        "CTRL2": 15,
        "CTRL3": 16,
        "CTRL4": 18,
        "TRIGGER": 22,
    },
}

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file or return defaults."""
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            user_config = json.load(f)
            return {**DEFAULT_CONFIG, **user_config}
    return DEFAULT_CONFIG
