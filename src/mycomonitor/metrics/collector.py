"""Metrics collection and monitoring for MycoMonitor."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

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

    def __init__(self, storage_path: str = "/var/log/mycomonitor/metrics") -> None:
        """
        Initialize metrics collector.
        
        Args:
            storage_path: Path to store metrics data
        """
        self.storage_path = Path(storage_path)
        self.current_metrics: Optional[SystemMetrics] = None
        self.initialize_storage()

    def initialize_storage(self) -> None:
        """Initialize metrics storage directory."""
        self.storage_path.mkdir(parents=True, exist_ok=True)

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
            timestamp=datetime.now().timestamp(),
            humidity_readings=humidity_data.copy(),
            temperature_readings=temperature_data.copy(),
            humidifier_state=humidifier_state,
            runtime=runtime,
            cycle_count=cycle_count,
            errors=errors.copy()
        )
        self._store_metrics()

    def _store_metrics(self) -> None:
        """Store current metrics to file."""
        if not self.current_metrics:
            return

        timestamp = datetime.fromtimestamp(self.current_metrics.timestamp)
        date_dir = self.storage_path / timestamp.strftime("%Y-%m")
        date_dir.mkdir(exist_ok=True)
        
        filename = date_dir / f"metrics_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

        with filename.open('w') as f:
            json.dump(vars(self.current_metrics), f, indent=4)

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
        metrics: List[SystemMetrics] = []
        current = start_time

        while current <= end_time:
            date_dir = self.storage_path / current.strftime("%Y-%m")
            
            if date_dir.exists():
                for filepath in date_dir.glob("*.json"):
                    if not filepath.name.endswith('.json'):
                        continue
                        
                    with filepath.open('r') as f:
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
    ) -> Dict[str, Any]:
        """
        Calculate statistics from a list of metrics.
        
        Args:
            metrics: List of SystemMetrics objects
            
        Returns:
            Dictionary of calculated statistics
        """
        if not metrics:
            return {}

        humidity_values: List[float] = []
        temperature_values: List[float] = []
        runtime_values: List[float] = []
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
