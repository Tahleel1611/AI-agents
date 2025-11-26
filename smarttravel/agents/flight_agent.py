"""Flight Agent - Handles flight search and recommendations

Specialized agent for finding and recommending flight options.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class FlightOption:
    """Data class for flight options"""
    airline: str
    departure_city: str
    arrival_city: str
    departure_time: str
    arrival_time: str
    price: float
    duration_hours: float
    stops: int = 0


class FlightAgent:
    """Agent specialized in flight search and recommendations
    
    Searches for flight options and provides recommendations based on
    user preferences like price, duration, and number of stops.
    """
    
    def __init__(self, config=None):
        """Initialize the Flight Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("FlightAgent initialized")
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1
    ) -> List[FlightOption]:
        """Search for available flights
        
        Args:
            origin: Departure city or airport code
            destination: Arrival city or airport code
            departure_date: Date of departure (YYYY-MM-DD)
            return_date: Optional return date for round trips
            passengers: Number of passengers
            
        Returns:
            List of FlightOption objects with available flights
        """
        logger.info(f"Searching flights from {origin} to {destination}")
        
        # Mock implementation - in production, this would call flight APIs
        flights = [
            FlightOption(
                airline="Mock Airlines",
                departure_city=origin,
                arrival_city=destination,
                departure_time=f"{departure_date}T08:00:00",
                arrival_time=f"{departure_date}T12:00:00",
                price=350.0 * passengers,
                duration_hours=4.0,
                stops=0
            ),
            FlightOption(
                airline="Budget Air",
                departure_city=origin,
                arrival_city=destination,
                departure_time=f"{departure_date}T14:00:00",
                arrival_time=f"{departure_date}T20:00:00",
                price=200.0 * passengers,
                duration_hours=6.0,
                stops=1
            )
        ]
        
        return flights
    
    def get_best_flight(
        self,
        flights: List[FlightOption],
        preference: str = "price"
    ) -> Optional[FlightOption]:
        """Get the best flight based on preference
        
        Args:
            flights: List of flight options to choose from
            preference: Sorting preference ('price', 'duration', 'stops')
            
        Returns:
            Best FlightOption based on preference, or None if no flights
        """
        if not flights:
            return None
        
        if preference == "price":
            return min(flights, key=lambda f: f.price)
        elif preference == "duration":
            return min(flights, key=lambda f: f.duration_hours)
        elif preference == "stops":
            return min(flights, key=lambda f: f.stops)
        
        return flights[0]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "FlightAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
