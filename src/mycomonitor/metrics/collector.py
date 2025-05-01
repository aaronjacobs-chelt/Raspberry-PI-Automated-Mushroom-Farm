"""Metrics collection and monitoring for MycoMonitor."""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os
from datetime import datetime, timedelta

@dataclass
class SystemMetrics:
    """System-wide metrics data."""
    timestamp: float
    humidity_readings: Dict[str, float]
    temperature_readings: Dict[str, float]
    humidifier_state: bool
    runtime: float
    cycle_count: int
    errors: List[str]

class MetricsCollector:
    """Collects and manages system metrics."""

    def __init__(self, storage_path: str = "/var/log/mycomonitor/metrics"):
        self.storage_path = storage_path
        self.current_metrics: Optional[SystemMetrics] = None
        self.initialize_storage()

    def initialize_storage(self) -> None:
        """Initialize metrics storage directory."""
        os.makedirs(self.storage_path, exist_ok=True)

    def collect_metrics(
        self,
        humidity_data: Dict[str, float],
        temperature_data: Dict[str, float],
        humidifier_state: bool,
        runtime: float,
        cycle_count: int,
        errors: List[str]
    ) -> None:
        """
        Collect current system metrics.
        
        Args:
            humidity_data: Current humidity readings
            temperature_data: Current temperature readings
            humidifier_state: Current state of humidifier
            runtime: Current runtime
            cycle_count: Number of cycles
            errors: List of current errors
        """
        self.current_metrics = SystemMetrics(
            timestamp=time.time(),
            humidity_readings=humidity_data,
            temperature_readings=temperature_data,
            humidifier_state=humidifier_state,
            runtime=runtime,
            cycle_count=cycle_count,
            errors=errors
        )
        self._store_metrics()

    def _store_metrics(self) -> None:
        """Store current metrics to file."""
        if not self.current_metrics:
            return

        # Create timestamp-based filename
        timestamp = datetime.fromtimestamp(self.current_metrics.timestamp)
        date_dir = os.path.join(
            self.storage_path,
            timestamp.strftime("%Y-%m")
        )
        os.makedirs(date_dir, exist_ok=True)
        
        filename = os.path.join(
            date_dir,
            f"metrics_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        )

        # Store metrics
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": self.current_metrics.timestamp,
                "humidity_readings": self.current_metrics.humidity_readings,
                "temperature_readings": self.current_metrics.temperature_readings,
                "humidifier_state": self.current_metrics.humidifier_state,
                "runtime": self.current_metrics.runtime,
                "cycle_count": self.current_metrics.cycle_count,
                "errors": self.current_metrics.errors
            }, f)

    def get_metrics_range(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[SystemMetrics]:
        """
        Retrieve metrics for a specific time range.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            
        Returns:
            List of SystemMetrics objects
        """
        metrics = []
        current = start_time

        while current <= end_time:
            date_dir = os.path.join(
                self.storage_path,
                current.strftime("%Y-%m")
            )
            
            if os.path.exists(date_dir):
                for filename in os.listdir(date_dir):
                    if not filename.endswith('.json'):
                        continue
                        
                    filepath = os.path.join(date_dir, filename)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        
                    metric_time = datetime.fromtimestamp(data["timestamp"])
                    if start_time <= metric_time <= end_time:
                        metrics.append(SystemMetrics(**data))

            current += timedelta(days=1)

        return sorted(metrics, key=lambda x: x.timestamp)

    def get_latest_metrics(self) -> Optional[SystemMetrics]:
        """
        Get the most recent metrics.
        
        Returns:
            Most recent SystemMetrics or None
        """
        return self.current_metrics

    def calculate_statistics(
        self,
        metrics: List[SystemMetrics]
    ) -> Dict[str, any]:
        """
        Calculate statistics from a list of metrics.
        
        Args:
            metrics: List of SystemMetrics objects
            
        Returns:
            Dictionary of calculated statistics
        """
        if not metrics:
            return {}

        humidity_values = []
        temperature_values = []
        runtime_values = []
        total_cycles = 0
        total_errors = 0

        for metric in metrics:
            humidity_values.extend(metric.humidity_readings.values())
            temperature_values.extend(metric.temperature_readings.values())
            runtime_values.append(metric.runtime)
            total_cycles += metric.cycle_count
            total_errors += len(metric.errors)

        return {
            "humidity": {
                "min": min(humidity_values) if humidity_values else None,
                "max": max(humidity_values) if humidity_values else None,
                "avg": sum(humidity_values) / len(humidity_values) if humidity_values else None
            },
            "temperature": {
                "min": min(temperature_values) if temperature_values else None,
                "max": max(temperature_values) if temperature_values else None,
                "avg": sum(temperature_values) / len(temperature_values) if temperature_values else None
            },
            "runtime": {
                "total": sum(runtime_values),
                "avg": sum(runtime_values) / len(runtime_values) if runtime_values else 0
            },
            "cycles": total_cycles,
            "errors": total_errors
        }

