"""SmartTravel AI - Multi-Agent Travel Concierge

A comprehensive AI-powered travel planning system using multiple specialized agents.
"""

__version__ = "1.0.0"
__author__ = "SmartTravel AI Team"

from .agents import TravelConcierge
from .config import Config

__all__ = ["TravelConcierge", "Config"]
