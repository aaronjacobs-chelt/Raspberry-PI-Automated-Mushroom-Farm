"""Tests for the HumidifierController class."""

import pytest
from unittest.mock import MagicMock, patch
from mycomonitor.core.controller import HumidifierController

@pytest.fixture
def mock_gpio():
    """Mock RPi.GPIO module."""
    with patch("mycomonitor.core.controller.GPIO") as mock:
        yield mock

@pytest.fixture
def controller(mock_gpio):
    """Create a HumidifierController instance with mocked GPIO."""
    return HumidifierController()

def test_init(controller, mock_gpio):
    """Test controller initialization."""
    assert controller.reboot_counter == 0
    assert controller.dry_counter == 0
    mock_gpio.setmode.assert_called_once_with(mock_gpio.BOARD)
    mock_gpio.setwarnings.assert_called_once_with(False)

def test_turn_on(controller, mock_gpio):
    """Test humidifier activation."""
    mock_gpio.input.return_value = True
    controller.turn_on()
    mock_gpio.output.assert_called()

def test_turn_off(controller, mock_gpio):
    """Test humidifier deactivation."""
    mock_gpio.input.return_value = False
    controller.turn_off()
    mock_gpio.output.assert_called()

def test_read_humidity(controller):
    """Test humidity reading from sensor file."""
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = \
            '{"sensor1": {"humidity": 85.5}}'
        humidity = controller.read_humidity("sensor1")
        assert humidity == 85.5
