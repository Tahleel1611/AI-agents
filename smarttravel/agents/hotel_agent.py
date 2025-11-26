"""Hotel Agent - Handles accommodation search and recommendations

Specialized agent for finding and recommending hotel accommodations.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class HotelOption:
    """Data class for hotel options"""
    name: str
    location: str
    star_rating: int
    price_per_night: float
    amenities: List[str]
    guest_rating: float = 0.0
    room_type: str = "Standard"


class HotelAgent:
    """Agent specialized in hotel search and recommendations
    
    Searches for accommodation options and provides recommendations based on
    user preferences like price, location, and amenities.
    """
    
    def __init__(self, config=None):
        """Initialize the Hotel Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("HotelAgent initialized")
    
    def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int = 1,
        rooms: int = 1
    ) -> List[HotelOption]:
        """Search for available hotels
        
        Args:
            destination: City or location to search
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            guests: Number of guests
            rooms: Number of rooms needed
            
        Returns:
            List of HotelOption objects with available accommodations
        """
        logger.info(f"Searching hotels in {destination}")
        
        # Mock implementation - in production, this would call hotel APIs
        hotels = [
            HotelOption(
                name="Grand Hotel",
                location=f"Downtown {destination}",
                star_rating=5,
                price_per_night=250.0,
                amenities=["WiFi", "Pool", "Spa", "Restaurant", "Gym"],
                guest_rating=4.8,
                room_type="Deluxe"
            ),
            HotelOption(
                name="City Inn",
                location=f"Central {destination}",
                star_rating=3,
                price_per_night=95.0,
                amenities=["WiFi", "Breakfast", "Parking"],
                guest_rating=4.2,
                room_type="Standard"
            ),
            HotelOption(
                name="Budget Stay",
                location=f"{destination} Suburbs",
                star_rating=2,
                price_per_night=55.0,
                amenities=["WiFi", "Parking"],
                guest_rating=3.8,
                room_type="Basic"
            )
        ]
        
        return hotels
    
    def get_best_hotel(
        self,
        hotels: List[HotelOption],
        preference: str = "rating"
    ) -> Optional[HotelOption]:
        """Get the best hotel based on preference
        
        Args:
            hotels: List of hotel options to choose from
            preference: Sorting preference ('price', 'rating', 'stars')
            
        Returns:
            Best HotelOption based on preference, or None if no hotels
        """
        if not hotels:
            return None
        
        if preference == "price":
            return min(hotels, key=lambda h: h.price_per_night)
        elif preference == "rating":
            return max(hotels, key=lambda h: h.guest_rating)
        elif preference == "stars":
            return max(hotels, key=lambda h: h.star_rating)
        
        return hotels[0]
    
    def calculate_total_cost(
        self,
        hotel: HotelOption,
        nights: int,
        rooms: int = 1
    ) -> float:
        """Calculate total accommodation cost
        
        Args:
            hotel: Selected hotel option
            nights: Number of nights
            rooms: Number of rooms
            
        Returns:
            Total cost for the stay
        """
        return hotel.price_per_night * nights * rooms
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "HotelAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
