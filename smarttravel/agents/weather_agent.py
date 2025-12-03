"""Weather Agent - Handles weather forecasts and climate information

Specialized agent for fetching weather data and providing travel weather insights.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class WeatherForecast:
    """Data class for weather forecasts"""
    date: str
    location: str
    temperature_high: float
    temperature_low: float
    condition: str  # e.g., "sunny", "rainy", "cloudy"
    precipitation_chance: float  # 0-100
    humidity: float  # 0-100
    wind_speed: float  # km/h
    description: str


class WeatherAgent:
    """Agent specialized in weather forecasts and climate recommendations
    
    Fetches weather data for destinations and provides insights for travel planning,
    including activity recommendations based on weather conditions.
    """
    
    def __init__(self, config=None):
        """Initialize the Weather Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("WeatherAgent initialized")
    
    def get_forecast(
        self,
        destination: str,
        start_date: str,
        end_date: str
    ) -> List[WeatherForecast]:
        """Get weather forecast for a destination and date range
        
        Args:
            destination: City or location
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            List of WeatherForecast objects
        """
        logger.info(f"Fetching weather forecast for {destination}")
        
        # Mock implementation - in production, this would call weather APIs
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        forecasts = []
        for i in range(days):
            forecast_date = start + timedelta(days=i)
            forecasts.append(
                WeatherForecast(
                    date=forecast_date.strftime("%Y-%m-%d"),
                    location=destination,
                    temperature_high=25.0 + (i % 5),
                    temperature_low=18.0 + (i % 3),
                    condition="sunny" if i % 2 == 0 else "partly cloudy",
                    precipitation_chance=20.0 + (i * 5),
                    humidity=60.0 + (i % 10),
                    wind_speed=15.0 + (i % 8),
                    description=f"Pleasant weather expected in {destination}"
                )
            )
        
        return forecasts
    
    def get_weather_summary(
        self,
        forecasts: List[WeatherForecast]
    ) -> Dict[str, Any]:
        """Generate weather summary for a trip
        
        Args:
            forecasts: List of weather forecasts
        
        Returns:
            Dictionary with weather summary statistics
        """
        if not forecasts:
            return {}
        
        avg_high = sum(f.temperature_high for f in forecasts) / len(forecasts)
        avg_low = sum(f.temperature_low for f in forecasts) / len(forecasts)
        max_precip = max(f.precipitation_chance for f in forecasts)
        rainy_days = len([f for f in forecasts if f.precipitation_chance > 50])
        
        return {
            "average_high": round(avg_high, 1),
            "average_low": round(avg_low, 1),
            "max_precipitation_chance": round(max_precip, 1),
            "rainy_days": rainy_days,
            "total_days": len(forecasts)
        }
    
    def get_weather_warnings(
        self,
        forecasts: List[WeatherForecast]
    ) -> List[str]:
        """Identify weather warnings and alerts
        
        Args:
            forecasts: List of weather forecasts
        
        Returns:
            List of warning messages
        """
        warnings = []
        
        for forecast in forecasts:
            if forecast.precipitation_chance > 70:
                warnings.append(
                    f"High chance of rain on {forecast.date} ({forecast.precipitation_chance}%)"
                )
            
            if forecast.temperature_high > 35:
                warnings.append(
                    f"Extreme heat expected on {forecast.date} ({forecast.temperature_high}°C)"
                )
            
            if forecast.temperature_low < 5:
                warnings.append(
                    f"Cold weather on {forecast.date} ({forecast.temperature_low}°C)"
                )
            
            if forecast.wind_speed > 40:
                warnings.append(
                    f"Strong winds on {forecast.date} ({forecast.wind_speed} km/h)"
                )
        
        return warnings
    
    def suggest_activity_adjustments(
        self,
        forecast: WeatherForecast
    ) -> Dict[str, Any]:
        """Suggest activity adjustments based on weather
        
        Args:
            forecast: Weather forecast for a specific day
        
        Returns:
            Dictionary with suggestions
        """
        suggestions = {
            "outdoor_suitable": True,
            "indoor_recommended": False,
            "advice": []
        }
        
        if forecast.precipitation_chance > 60:
            suggestions["outdoor_suitable"] = False
            suggestions["indoor_recommended"] = True
            suggestions["advice"].append("Consider indoor activities like museums")
        
        if forecast.temperature_high > 32:
            suggestions["advice"].append("Stay hydrated and avoid midday sun")
            suggestions["advice"].append("Plan outdoor activities for morning/evening")
        
        if forecast.temperature_low < 10:
            suggestions["advice"].append("Bring warm clothing for cooler temperatures")
        
        if not suggestions["advice"]:
            suggestions["advice"].append("Great day for outdoor exploration!")
        
        return suggestions
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "WeatherAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
