"""Core controller for MycoMonitor system."""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

import RPi.GPIO as GPIO

from ..safety.monitor import SafetyMonitor
from ..metrics.collector import MetricsCollector
from ..utils.config import load_config
from ..utils.logging import setup_logging

class HumidifierController:
    """Main controller for the humidifier system."""
    
    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialize the controller.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config: Dict[str, Any] = load_config(config_path)
        self.reboot_counter: int = 0
        self.dry_counter: int = 0
        self._setup_gpio()
        self._setup_monitoring()
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Controller initialized")

    def _setup_gpio(self) -> None:
        """Initialize GPIO settings."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        for pin in self.config["gpio_pins"].values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        self.logger.info("GPIO setup complete")

    def _setup_monitoring(self) -> None:
        """Initialize monitoring systems."""
        self.safety_monitor = SafetyMonitor(self.config)
        self.metrics_collector = MetricsCollector()
        self.last_check_time: float = time.time()
        self.total_runtime: float = 0.0
        self.cycle_count: int = 0
        self.errors: List[str] = []

    def cleanup_and_reboot(self) -> None:
        """Clean up GPIO and reboot system."""
        self.logger.info("Cleaning up GPIO and rebooting system")
        self.turn_off()
        GPIO.cleanup()
        os.system("sudo reboot")

    def send_signal(
        self,
        pins: List[int],
        delay1: float = 0.1,
        delay2: float = 0.25
    ) -> None:
        """
        Send control signal to GPIO pins.
        
        Args:
            pins: List of GPIO pins to control
            delay1: First delay duration
            delay2: Second delay duration
        """
        try:
            for pin in pins:
                GPIO.output(pin, True)
            time.sleep(delay1)
            GPIO.output(self.config["gpio_pins"]["TRIGGER"], True)
            time.sleep(delay2)
            GPIO.output(self.config["gpio_pins"]["TRIGGER"], False)
        except Exception as e:
            self.logger.error(f"Error sending signal: {e}")
            self.errors.append(f"Signal error: {str(e)}")
            raise

    def turn_on(self) -> None:
        """Activate the humidifier."""
        try:
            self._send_on_signal()
            retry_count = 0
            while not self._verify_on_state() and retry_count < 3:
                self.logger.warning("Retrying humidifier activation")
                time.sleep(5)
                self._send_on_signal()
                retry_count += 1
            
            if not self._verify_on_state():
                raise RuntimeError("Failed to activate humidifier")
            
            self.cycle_count += 1
            self._update_metrics(True)
        except Exception as e:
            self.logger.error(f"Error turning on humidifier: {e}")
            self.errors.append(f"Activation error: {str(e)}")
            raise

    def turn_off(self) -> None:
        """Deactivate the humidifier."""
        try:
            self._send_off_signal()
            retry_count = 0
            while not self._verify_off_state() and retry_count < 3:
                self.logger.warning("Retrying humidifier deactivation")
                self._send_off_signal()
                time.sleep(5)
                retry_count += 1
            
            if not self._verify_off_state():
                raise RuntimeError("Failed to deactivate humidifier")
            
            self._update_metrics(False)
        except Exception as e:
            self.logger.error(f"Error turning off humidifier: {e}")
            self.errors.append(f"Deactivation error: {str(e)}")
            raise

    def _send_on_signal(self) -> None:
        """Send the activation signal."""
        pins = [
            self.config["gpio_pins"]["CTRL1"],
            self.config["gpio_pins"]["CTRL2"],
            self.config["gpio_pins"]["CTRL3"],
            self.config["gpio_pins"]["OUTLET"]
        ]
        self.send_signal(pins)
        self.logger.info("Humidifier ON signal sent")

    def _send_off_signal(self) -> None:
        """Send the deactivation signal."""
        pins = [
            self.config["gpio_pins"]["CTRL1"],
            self.config["gpio_pins"]["CTRL2"],
            self.config["gpio_pins"]["CTRL3"]
        ]
        self.send_signal(pins)
        GPIO.output(self.config["gpio_pins"]["OUTLET"], False)
        time.sleep(0.25)
        self.logger.info("Humidifier OFF signal sent")

    def _verify_on_state(self) -> bool:
        """Verify humidifier is on."""
        return GPIO.input(self.config["gpio_pins"]["OUTLET"]) is True

    def _verify_off_state(self) -> bool:
        """Verify humidifier is off."""
        return GPIO.input(self.config["gpio_pins"]["OUTLET"]) is False

    def read_sensor_data(self) -> Dict[str, Dict[str, float]]:
        """
        Read data from all sensors.
        
        Returns:
            Dictionary of sensor readings
        """
        try:
            with open(self.config["sensor_file"]) as f:
                data = json.load(f)
            
            readings: Dict[str, Dict[str, float]] = {}
            for sensor_id in self.config["sensor_names"]:
                if sensor_id in data:
                    readings[sensor_id] = {
                        "humidity": float(data[sensor_id]["humidity"]),
                        "temperature": float(data[sensor_id].get("temperature", 20.0))
                    }
            return readings
        except Exception as e:
            self.logger.error(f"Failed to read sensors: {e}")
            self.errors.append(f"Sensor read error: {str(e)}")
            raise

    def _update_metrics(self, active: bool) -> None:
        """
        Update system metrics.
        
        Args:
            active: Whether the humidifier is active
        """
        try:
            readings = self.read_sensor_data()
            humidity_readings = {
                sensor_id: data["humidity"]
                for sensor_id, data in readings.items()
            }
            temperature_readings = {
                sensor_id: data["temperature"]
                for sensor_id, data in readings.items()
            }
            
            self.metrics_collector.collect_metrics(
                humidity_data=humidity_readings,
                temperature_data=temperature_readings,
                humidifier_state=active,
                runtime=self.total_runtime,
                cycle_count=self.cycle_count,
                errors=self.errors.copy()
            )
        except Exception as e:
            self.logger.error(f"Error updating metrics: {e}")
            self.errors.append(f"Metrics error: {str(e)}")

    def run(self) -> None:
        """Main control loop."""
        try:
            while self.reboot_counter <= self.config["cycle_reboot_limit"]:
                try:
                    readings = self.read_sensor_data()
                    
                    # Safety checks
                    is_safe, warnings = self.safety_monitor.check_sensor_readings(readings)
                    for warning in warnings:
                        self.logger.warning(warning)
                    
                    if not is_safe:
                        self.safety_monitor.emergency_shutdown("Unsafe conditions detected")
                        break

                    # Process readings
                    low_humidity = any(
                        data["humidity"] < self.config["humidity_threshold"]
                        for data in readings.values()
                    )

                    if low_humidity:
                        self.logger.info(f"Low humidity detected: {readings}")
                        for _ in range(3):
                            self.turn_on()
                            time.sleep(self.config["activation_time"])
                            self.turn_off()
                            time.sleep(60)
                        time.sleep(180)
                    else:
                        self.logger.info(f"Humidity OK: {readings}")
                    
                    self.reboot_counter += 1
                    self._handle_data_freshness(readings)

                except Exception as e:
                    self.logger.error(f"Error in control loop: {e}")
                    self.errors.append(f"Control error: {str(e)}")
                    time.sleep(60)  # Wait before retrying

        except Exception as e:
            self.logger.critical(f"Critical error: {e}")
            self.errors.append(f"Critical error: {str(e)}")
        finally:
            self.cleanup_and_reboot()

    def _handle_data_freshness(
        self,
        prev_readings: Dict[str, Dict[str, float]]
    ) -> None:
        """
        Handle data freshness checking.
        
        Args:
            prev_readings: Previous sensor readings
        """
        while True:
            time.sleep(120)
            try:
                new_readings = self.read_sensor_data()
                if new_readings != prev_readings:
                    self.dry_counter = 0
                    break
                
                self.dry_counter += 1
                self.logger.warning(
                    f"No new sensor data for {self.dry_counter * 2} minutes"
                )
                
                if self.dry_counter >= self.config["stale_data_threshold"]:
                    self.logger.warning(
                        "Stale data threshold reached — activating humidifier as fallback"
                    )
                    self.turn_on()
                    time.sleep(self.config["activation_time"])
                    self.turn_off()
                    self.dry_counter = 0
                    break
            except Exception as e:
                self.logger.error(f"Error checking data freshness: {e}")
                self.errors.append(f"Freshness check error: {str(e)}")
                time.sleep(60)

