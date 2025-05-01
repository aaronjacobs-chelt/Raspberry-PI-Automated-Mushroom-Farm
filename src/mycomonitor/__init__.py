"""MycoMonitor - Automated mushroom cultivation environment controller."""

__version__ = "1.0.0"
__author__ = "Aaron Jacobs"
__email__ = "git@happycaps.co.uk"

from .core.controller import HumidifierController

__all__ = ["HumidifierController"]
