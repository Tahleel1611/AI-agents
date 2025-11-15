"""Configuration settings for SmartTravel AI"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Main configuration class for SmartTravel AI"""
    
    # API Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Agent Configuration
    model_name: str = "gemini-1.5-pro"
    temperature: float = 0.7
    top_p: float = 0.95
    
    # Travel Services API Keys (optional)
    skyscanner_api_key: Optional[str] = os.getenv("SKYSCANNER_API_KEY")
    booking_com_api_key: Optional[str] = os.getenv("BOOKING_COM_API_KEY")
    google_maps_api_key: Optional[str] = os.getenv("GOOGLE_MAPS_API_KEY")
    
    # System Configuration
    max_retries: int = 3
    timeout: int = 30
    debug_mode: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True


# Default configuration instance
config = Config()
