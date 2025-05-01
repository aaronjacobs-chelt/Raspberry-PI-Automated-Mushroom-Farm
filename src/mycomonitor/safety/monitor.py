"""Safety monitoring and emergency shutdown system."""

import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ..utils.config import load_config

@dataclass
class SafetyThresholds:
    """Safety thresholds for the system."""
    max_humidity: float = 98.0
    min_humidity: float = 40.0
    max_temperature: float = 30.0
    min_temperature: float = 10.0
    max_runtime: int = 300  # seconds
    min_cycle_interval: int = 60  # seconds
    stale_data_timeout: int = 300  # seconds

class SafetyMonitor:
    """Monitors system safety and triggers emergency procedures when needed."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = load_config(config_path)
        self.thresholds = SafetyThresholds(
            max_humidity=self.config.get("safety", {}).get("max_humidity", 98.0),
            min_humidity=self.config.get("safety", {}).get("min_humidity", 40.0),
            max_temperature=self.config.get("safety", {}).get("max_temperature", 30.0),
            min_temperature=self.config.get("safety", {}).get("min_temperature", 10.0),
            max_runtime=self.config.get("safety", {}).get("max_runtime", 300),
            min_cycle_interval=self.config.get("safety", {}).get("min_cycle_interval", 60),
            stale_data_timeout=self.config.get("safety", {}).get("stale_data_timeout", 300)
        )
        self.last_check_time: float = time.time()
        self.last_activation_time: float = 0
        self.current_runtime: float = 0
        self.emergency_mode: bool = False
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up safety-specific logging."""
        self.logger = logging.getLogger("mycomonitor.safety")
        self.logger.setLevel(logging.INFO)

    def check_sensor_readings(
        self, readings: Dict[str, Dict[str, float]]
    ) -> Tuple[bool, List[str]]:
        """
        Check if sensor readings are within safe ranges.
        
        Args:
            readings: Dictionary of sensor readings
            
        Returns:
            Tuple of (is_safe, list of warnings)
        """
        warnings = []
        is_safe = True

        for sensor_id, data in readings.items():
            # Check humidity
            if "humidity" in data:
                humidity = data["humidity"]
                if humidity > self.thresholds.max_humidity:
                    warnings.append(f"Humidity too high: {humidity}% on {sensor_id}")
                    is_safe = False
                elif humidity < self.thresholds.min_humidity:
                    warnings.append(f"Humidity too low: {humidity}% on {sensor_id}")

            # Check temperature if available
            if "temperature" in data:
                temp = data["temperature"]
                if temp > self.thresholds.max_temperature:
                    warnings.append(f"Temperature too high: {temp}°C on {sensor_id}")
                    is_safe = False
                elif temp < self.thresholds.min_temperature:
                    warnings.append(f"Temperature too low: {temp}°C on {sensor_id}")

        return is_safe, warnings

    def check_runtime(self, active: bool) -> Tuple[bool, List[str]]:
        """Check if runtime is within safe limits."""
        warnings = []
        is_safe = True
        current_time = time.time()

        if active:
            self.current_runtime = current_time - self.last_activation_time
            if self.current_runtime > self.thresholds.max_runtime:
                warnings.append(
                    f"Maximum runtime exceeded: {self.current_runtime:.1f}s"
                )
                is_safe = False
        else:
            self.current_runtime = 0
            self.last_activation_time = current_time

        return is_safe, warnings

    def check_cycle_interval(self) -> Tuple[bool, List[str]]:
        """Check if cycle interval is safe."""
        warnings = []
        is_safe = True
        current_time = time.time()

        if (current_time - self.last_activation_time) < self.thresholds.min_cycle_interval:
            warnings.append("Cycle interval too short")
            is_safe = False

        return is_safe, warnings

    def check_data_freshness(self, last_update_time: float) -> Tuple[bool, List[str]]:
        """Check if sensor data is fresh enough."""
        warnings = []
        is_safe = True
        current_time = time.time()

        if (current_time - last_update_time) > self.thresholds.stale_data_timeout:
            warnings.append("Sensor data is stale")
            is_safe = False

        return is_safe, warnings

    def emergency_shutdown(self, reason: str) -> None:
        """
        Perform emergency shutdown procedure.
        
        Args:
            reason: Reason for emergency shutdown
        """
        if not self.emergency_mode:
            self.emergency_mode = True
            self.logger.critical(f"EMERGENCY SHUTDOWN: {reason}")
            # Implement shutdown logic here
            # This should be implemented by the main controller

    def reset_emergency_mode(self) -> None:
        """Reset emergency mode after safety checks pass."""
        if self.emergency_mode:
            self.emergency_mode = False
            self.logger.info("Emergency mode reset - system returning to normal operation")

