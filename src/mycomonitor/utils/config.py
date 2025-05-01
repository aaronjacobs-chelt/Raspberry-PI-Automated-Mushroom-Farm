"""Configuration management for MycoMonitor."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class SystemConfig:
    """System configuration structure."""
    humidity_threshold: float
    activation_time: int
    cycle_reboot_limit: int
    stale_data_threshold: int
    sensor_names: list[str]
    gpio_pins: Dict[str, int]
    log_file: str
    log_level: str
    data_dir: str
    sensor_file: str

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
    "log_file": "/var/log/mycomonitor/mycomonitor.log",
    "log_level": "INFO",
    "data_dir": "/var/lib/mycomonitor",
    "sensor_file": "/opt/zigbee2mqtt/data/state.json"
}

def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration values.
    
    Args:
        config: Configuration dictionary to validate
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_fields = [
        "humidity_threshold",
        "activation_time",
        "cycle_reboot_limit",
        "gpio_pins",
        "sensor_names"
    ]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")
    
    if not isinstance(config["humidity_threshold"], (int, float)):
        raise ValueError("humidity_threshold must be a number")
    
    if not isinstance(config["gpio_pins"], dict):
        raise ValueError("gpio_pins must be a dictionary")
    
    required_pins = ["OUTLET", "CTRL1", "CTRL2", "CTRL3", "TRIGGER"]
    for pin in required_pins:
        if pin not in config["gpio_pins"]:
            raise ValueError(f"Missing required GPIO pin: {pin}")

def load_config(config_path: Optional[str] = None) -> SystemConfig:
    """
    Load configuration from file or return defaults.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        SystemConfig object with loaded configuration
        
    Raises:
        ValueError: If configuration is invalid
    """
    config_dict = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path) as f:
                user_config = json.load(f)
                config_dict.update(user_config)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading config file: {e}")
    
    # Ensure data directory exists
    data_dir = Path(config_dict["data_dir"])
    data_dir.mkdir(parents=True, exist_ok=True)
    
    validate_config(config_dict)
    return SystemConfig(**config_dict)

def save_config(config: SystemConfig, config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config: SystemConfig object to save
        config_path: Path to save configuration file
        
    Raises:
        ValueError: If configuration cannot be saved
    """
    try:
        config_dict = {
            k: v for k, v in config.__dict__.items()
            if not k.startswith('_')
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)
    except Exception as e:
        raise ValueError(f"Error saving config file: {e}")
