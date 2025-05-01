"""Tests for configuration management."""

import pytest
from mycomonitor.utils.config import load_config, DEFAULT_CONFIG

def test_load_default_config():
    """Test loading default configuration."""
    config = load_config()
    assert config == DEFAULT_CONFIG
    assert config["humidity_threshold"] == 95.0

def test_load_custom_config(tmp_path):
    """Test loading custom configuration."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"humidity_threshold": 90.0}')
    
    config = load_config(str(config_file))
    assert config["humidity_threshold"] == 90.0
    assert config["activation_time"] == DEFAULT_CONFIG["activation_time"]
