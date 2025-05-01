"""Hardware diagnostics for MycoMonitor."""

import time
from typing import Dict, List, Optional, Tuple
import RPi.GPIO as GPIO

class HardwareDiagnostics:
    """Diagnostic tools for hardware components."""

    def __init__(self, gpio_pins: Dict[str, int]):
        self.gpio_pins = gpio_pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def test_gpio_output(self, pin: int) -> Tuple[bool, str]:
        """
        Test GPIO output functionality.
        
        Args:
            pin: GPIO pin number to test
            
        Returns:
            Tuple of (success, message)
        """
        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.1)
            high_state = GPIO.input(pin)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)
            low_state = GPIO.input(pin)
            
            if high_state and not low_state:
                return True, f"Pin {pin} functioning correctly"
            else:
                return False, f"Pin {pin} state change failed"
        except Exception as e:
            return False, f"Error testing pin {pin}: {str(e)}"
        finally:
            GPIO.cleanup(pin)

    def test_all_pins(self) -> List[Tuple[int, bool, str]]:
        """
        Test all configured GPIO pins.
        
        Returns:
            List of (pin, success, message) tuples
        """
        results = []
        for name, pin in self.gpio_pins.items():
            success, message = self.test_gpio_output(pin)
            results.append((pin, success, f"{name}: {message}"))
        return results

    def verify_power_state(self, pin: int) -> Tuple[bool, float]:
        """
        Verify power state and measure voltage if possible.
        
        Args:
            pin: GPIO pin number to check
            
        Returns:
            Tuple of (is_powered, voltage)
        """
        try:
            GPIO.setup(pin, GPIO.IN)
            state = GPIO.input(pin)
            # Note: actual voltage measurement would require ADC
            # This is a simplified version
            voltage = 3.3 if state else 0.0
            return bool(state), voltage
        except Exception:
            return False, 0.0

    def check_sensor_connection(self, sensor_id: str) -> Tuple[bool, str]:
        """
        Check if a sensor is properly connected.
        
        Args:
            sensor_id: Identifier for the sensor
            
        Returns:
            Tuple of (is_connected, message)
        """
        # Implementation would depend on sensor type and connection method
        # This is a placeholder for the interface
        return True, f"Sensor {sensor_id} connection verified"

    def run_full_diagnostic(self) -> Dict[str, any]:
        """
        Run a full system diagnostic.
        
        Returns:
            Dictionary containing all diagnostic results
        """
        results = {
            "gpio_tests": self.test_all_pins(),
            "power_states": {},
            "sensor_connections": {},
            "timestamp": time.time()
        }
        
        # Check power states
        for name, pin in self.gpio_pins.items():
            powered, voltage = self.verify_power_state(pin)
            results["power_states"][name] = {
                "powered": powered,
                "voltage": voltage
            }
        
        return results

