"""Integration tests for the full MycoMonitor system."""

import pytest
import json
import os
from mycomonitor.core import HumidifierController
from mycomonitor.utils import load_config, setup_logging

@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary configuration file."""
    config = {
        "humidity_threshold": 90.0,
        "activation_time": 5,
        "cycle_reboot_limit": 2,
        "stale_data_threshold": 2,
        "sensor_names": ["test_sensor"],
        "gpio_pins": {
            "OUTLET": 13,
            "CTRL1": 11,
            "CTRL2": 15,
            "CTRL3": 16,
            "CTRL4": 18,
            "TRIGGER": 22
        }
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config))
    return str(config_file)

@pytest.fixture
def temp_state(tmp_path):
    """Create a temporary state file."""
    state = {
        "test_sensor": {
            "humidity": 85.0,
            "temperature": 23.0,
            "battery": 100
        }
    }
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps(state))
    return str(state_file)

def test_full_system_cycle(temp_config, temp_state, monkeypatch):
    """Test a complete system cycle with configuration and state management."""
    # Mock GPIO
    monkeypatch.setenv("READTHEDOCS", "True")
    
    # Load configuration
    config = load_config(temp_config)
    
    # Setup logging
    setup_logging(log_file=None)  # Use console logging for tests
    
    # Initialize controller
    controller = HumidifierController()
    
    # Test humidity reading
    humidity = controller.read_humidity("test_sensor")
    assert humidity == 85.0
    
    # Test response to low humidity
    # ... Add more integration test steps
