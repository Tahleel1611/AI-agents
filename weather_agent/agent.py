"""Weather Agent - Provides weather information using AI"""

import os
import google.generativeai as genai
from typing import Optional, Dict


class WeatherAgent:
    """An AI-powered agent that provides weather information and insights."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Weather Agent.
        
        Args:
            api_key: Google API key. If not provided, will try to read from environment.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in GOOGLE_API_KEY environment variable")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_weather_info(self, location: str, query_type: str = "current") -> Dict:
        """Get weather information for a location.
        
        Args:
            location: The location to get weather for
            query_type: Type of query (current, forecast, historical)
            
        Returns:
            Dictionary containing weather information
        """
        prompt = f"""Provide {query_type} weather information for {location}.
        Include temperature, conditions, humidity, and any relevant alerts.
        Format the response as a brief, informative summary."""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'status': 'success',
                'location': location,
                'query_type': query_type,
                'weather_info': response.text
            }
        except Exception as e:
            return {
                'status': 'error',
                'location': location,
                'error': str(e)
            }
    
    def analyze_weather_patterns(self, location: str, days: int = 7) -> str:
        """Analyze weather patterns for a location.
        
        Args:
            location: The location to analyze
            days: Number of days to analyze
            
        Returns:
            Weather pattern analysis
        """
        prompt = f"""Analyze the typical weather patterns for {location} over the next {days} days.
        Include insights about temperature trends, precipitation likelihood, and seasonal considerations."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing weather patterns: {str(e)}"


if __name__ == "__main__":
    # Example usage
    agent = WeatherAgent()
    result = agent.get_weather_info("London, UK")
    print(result)
