"""MycoMonitor - Automated mushroom cultivation environment controller."""

from importlib.metadata import version, PackageNotFoundError
from typing import Optional

try:
    __version__ = version("mycomonitor")
except PackageNotFoundError:
    __version__ = "unknown"

from .core.controller import HumidifierController
from .utils.config import SystemConfig, load_config
from .safety.monitor import SafetyMonitor, SafetyThresholds
from .metrics.collector import MetricsCollector, SystemMetrics

__all__ = [
    "HumidifierController",
    "SystemConfig",
    "load_config",
    "SafetyMonitor",
    "SafetyThresholds",
    "MetricsCollector",
    "SystemMetrics",
]
