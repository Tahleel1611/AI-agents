"""Attraction Agent - Handles local attractions and activities

Specialized agent for discovering and recommending local attractions.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Attraction:
    """Data class for attractions"""
    name: str
    category: str
    location: str
    description: str
    rating: float
    price: float = 0.0
    duration_hours: float = 2.0
    open_hours: str = "09:00-18:00"


class AttractionAgent:
    """Agent specialized in attraction discovery and recommendations
    
    Discovers local attractions and activities, providing recommendations
    based on user interests and preferences.
    """
    
    def __init__(self, config=None):
        """Initialize the Attraction Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("AttractionAgent initialized")
    
    def discover_attractions(
        self,
        destination: str,
        categories: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[Attraction]:
        """Discover attractions in a destination
        
        Args:
            destination: City or location to search
            categories: Filter by categories (e.g., ['museum', 'park', 'landmark'])
            max_results: Maximum number of results to return
            
        Returns:
            List of Attraction objects
        """
        logger.info(f"Discovering attractions in {destination}")
        
        # Mock implementation - in production, this would call travel APIs
        all_attractions = [
            Attraction(
                name=f"{destination} Museum of Art",
                category="museum",
                location=f"Cultural District, {destination}",
                description="World-renowned art museum with extensive collections",
                rating=4.7,
                price=25.0,
                duration_hours=3.0
            ),
            Attraction(
                name=f"{destination} Central Park",
                category="park",
                location=f"City Center, {destination}",
                description="Beautiful urban park perfect for relaxation",
                rating=4.5,
                price=0.0,
                duration_hours=2.0
            ),
            Attraction(
                name=f"Historic {destination} Tower",
                category="landmark",
                location=f"Old Town, {destination}",
                description="Iconic landmark with panoramic city views",
                rating=4.8,
                price=15.0,
                duration_hours=1.5
            ),
            Attraction(
                name=f"{destination} Food Market",
                category="food",
                location=f"Market District, {destination}",
                description="Vibrant food market with local specialties",
                rating=4.6,
                price=0.0,
                duration_hours=2.0
            ),
            Attraction(
                name=f"{destination} Walking Tour",
                category="tour",
                location=f"Various locations, {destination}",
                description="Guided walking tour through historic neighborhoods",
                rating=4.4,
                price=35.0,
                duration_hours=3.0
            )
        ]
        
        # Filter by categories if specified
        if categories:
            all_attractions = [
                a for a in all_attractions 
                if a.category in categories
            ]
        
        return all_attractions[:max_results]
    
    def get_top_attractions(
        self,
        attractions: List[Attraction],
        count: int = 5
    ) -> List[Attraction]:
        """Get top-rated attractions
        
        Args:
            attractions: List of attractions to choose from
            count: Number of top attractions to return
            
        Returns:
            List of top-rated Attraction objects
        """
        sorted_attractions = sorted(
            attractions, 
            key=lambda a: a.rating, 
            reverse=True
        )
        return sorted_attractions[:count]
    
    def calculate_activities_cost(
        self,
        attractions: List[Attraction]
    ) -> float:
        """Calculate total cost for selected attractions
        
        Args:
            attractions: List of selected attractions
            
        Returns:
            Total cost for all attractions
        """
        return sum(a.price for a in attractions)
    
    def estimate_time_needed(
        self,
        attractions: List[Attraction]
    ) -> float:
        """Estimate total time needed for attractions
        
        Args:
            attractions: List of selected attractions
            
        Returns:
            Total hours needed
        """
        return sum(a.duration_hours for a in attractions)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "AttractionAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
