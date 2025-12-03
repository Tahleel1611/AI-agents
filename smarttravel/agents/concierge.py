"""Travel Concierge Agent - Main orchestration agent

Coordinates multiple specialized agents to provide comprehensive travel planning.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .flight_agent import FlightAgent
from .hotel_agent import HotelAgent
from .attraction_agent import AttractionAgent
from .itinerary_agent import ItineraryAgent
from .weather_agent import WeatherAgent


logger = logging.getLogger(__name__)


@dataclass
class TravelRequest:
    """Data class for travel requests"""
    destination: str
    start_date: str
    end_date: str
    origin: str = ""
    budget: Optional[float] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    travelers: int = 1


@dataclass
class TravelItinerary:
    """Data class for travel itinerary"""
    destination: str
    duration_days: int
    flights: List[Dict] = field(default_factory=list)
    accommodations: List[Dict] = field(default_factory=list)
    attractions: List[Dict] = field(default_factory=list)
    daily_schedule: List[Dict] = field(default_factory=list)
    total_estimated_cost: float = 0.0


class TravelConcierge:
    """Main travel concierge agent
    
    Orchestrates multiple specialized agents to create comprehensive travel itineraries.
    """
    
    def __init__(self, config=None):
        """Initialize the Travel Concierge
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        
        # Initialize specialized agents
        self.flight_agent = FlightAgent(config)
        self.hotel_agent = HotelAgent(config)
        self.attraction_agent = AttractionAgent(config)
        self.itinerary_agent = ItineraryAgent(config)
        
        logger.info("TravelConcierge initialized with all agents")
    
    def process_request(self, request: TravelRequest) -> TravelItinerary:
        """Process a travel request and generate an itinerary
        
        Args:
            request: TravelRequest object with travel details
            
        Returns:
            TravelItinerary: Comprehensive travel itinerary
        """
        logger.info(f"Processing travel request for {request.destination}")
        
        # Calculate duration
        duration = self._calculate_duration(request.start_date, request.end_date)
        
        # Search for flights if origin is provided
        flights = []
        if request.origin:
            flight_options = self.flight_agent.search_flights(
                origin=request.origin,
                destination=request.destination,
                departure_date=request.start_date,
                passengers=request.travelers
            )
            flights = [
                {
                    "airline": f.airline,
                    "departure": f.departure_time,
                    "arrival": f.arrival_time,
                    "price": f.price
                }
                for f in flight_options
            ]
        
        # Search for accommodations
        hotel_options = self.hotel_agent.search_hotels(
            destination=request.destination,
            check_in=request.start_date,
            check_out=request.end_date,
            guests=request.travelers
        )
        accommodations = [
            {
                "name": h.name,
                "location": h.location,
                "price_per_night": h.price_per_night,
                "rating": h.guest_rating
            }
            for h in hotel_options
        ]
        
        # Discover attractions
        categories = request.preferences.get("attraction_types") if request.preferences else None
        attraction_options = self.attraction_agent.discover_attractions(
            destination=request.destination,
            categories=categories
        )
        attractions = [
            {
                "name": a.name,
                "category": a.category,
                "description": a.description,
                "price": a.price
            }
            for a in attraction_options
        ]
        
        # Create itinerary with attractions
        itinerary_obj = self.itinerary_agent.create_itinerary(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            attractions=attraction_options,
            preferences=request.preferences
        )
        daily_schedule = [
            {
                "day": day.day_number,
                "date": day.date,
                "activities": day.activities
            }
            for day in itinerary_obj.days
        ]
        
        # Calculate total estimated cost
        total_cost = 0.0
        if flights:
            total_cost += min(f["price"] for f in flights)
        if accommodations:
            best_hotel = self.hotel_agent.get_best_hotel(hotel_options, "price")
            if best_hotel:
                total_cost += self.hotel_agent.calculate_total_cost(
                    best_hotel, duration
                )
        total_cost += self.attraction_agent.calculate_activities_cost(attraction_options)
        
        # Create final itinerary
        travel_itinerary = TravelItinerary(
            destination=request.destination,
            duration_days=duration,
            flights=flights,
            accommodations=accommodations,
            attractions=attractions,
            daily_schedule=daily_schedule,
            total_estimated_cost=total_cost
        )
        
        return travel_itinerary
    
    def _calculate_duration(self, start_date: str, end_date: str) -> int:
        """Calculate duration between dates
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Number of days between dates (inclusive)
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return (end - start).days + 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "status": "active",
            "initialized_at": self.initialized_at.isoformat(),
            "version": "1.0.0",
            "agents": {
                "flight": self.flight_agent.get_status(),
                "hotel": self.hotel_agent.get_status(),
                "attraction": self.attraction_agent.get_status(),
                "itinerary": self.itinerary_agent.get_status()
            }
        }
