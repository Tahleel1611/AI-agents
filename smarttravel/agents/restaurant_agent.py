"""Restaurant Agent - Handles dining recommendations and restaurant discovery

Specialized agent for discovering and recommending restaurants based on
cuisine preferences, dietary restrictions, and budget constraints.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Restaurant:
    """Data class for restaurants"""
    name: str
    cuisine: str
    location: str
    description: str
    rating: float
    price_range: str  # "$", "$$", "$$$", "$$$$"
    average_cost_per_person: float
    dietary_options: List[str]  # ["vegetarian", "vegan", "gluten-free", etc.]
    open_hours: str = "11:00-22:00"
    reservations_required: bool = False
    distance_km: float = 0.0


class RestaurantAgent:
    """Agent specialized in restaurant discovery and dining recommendations
    
    Discovers restaurants and provides personalized recommendations based on
    user preferences, dietary restrictions, and budget constraints.
    """
    
    def __init__(self, config=None):
        """Initialize the Restaurant Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("RestaurantAgent initialized")
    
    def discover_restaurants(
        self,
        destination: str,
        cuisines: Optional[List[str]] = None,
        dietary_restrictions: Optional[List[str]] = None,
        price_range: Optional[str] = None,
        max_results: int = 10
    ) -> List[Restaurant]:
        """Discover restaurants in a destination
        
        Args:
            destination: City or location to search
            cuisines: Filter by cuisine types (e.g., ['italian', 'japanese', 'indian'])
            dietary_restrictions: Filter by dietary options (e.g., ['vegetarian', 'vegan'])
            price_range: Filter by price range ("$", "$$", "$$$", "$$$$")
            max_results: Maximum number of results to return
        
        Returns:
            List of Restaurant objects
        """
        logger.info(f"Discovering restaurants in {destination}")
        
        # Mock implementation - in production, this would call restaurant APIs
        # (e.g., Yelp, Google Places, TripAdvisor)
        all_restaurants = [
            Restaurant(
                name=f"La Bella {destination}",
                cuisine="italian",
                location=f"Downtown, {destination}",
                description="Authentic Italian cuisine with fresh pasta and wood-fired pizzas",
                rating=4.6,
                price_range="$$",
                average_cost_per_person=35.0,
                dietary_options=["vegetarian", "gluten-free"],
                reservations_required=True,
                distance_km=1.2
            ),
            Restaurant(
                name=f"{destination} Sushi Bar",
                cuisine="japanese",
                location=f"Financial District, {destination}",
                description="Modern Japanese restaurant with sushi bar and omakase menu",
                rating=4.8,
                price_range="$$$",
                average_cost_per_person=65.0,
                dietary_options=["gluten-free"],
                reservations_required=True,
                distance_km=0.8
            ),
            Restaurant(
                name=f"Spice of {destination}",
                cuisine="indian",
                location=f"Cultural Quarter, {destination}",
                description="Traditional Indian restaurant with regional specialties",
                rating=4.5,
                price_range="$$",
                average_cost_per_person=30.0,
                dietary_options=["vegetarian", "vegan", "gluten-free"],
                reservations_required=False,
                distance_km=2.1
            ),
            Restaurant(
                name=f"Green Garden Bistro",
                cuisine="vegetarian",
                location=f"Arts District, {destination}",
                description="Plant-based restaurant with creative vegetarian dishes",
                rating=4.7,
                price_range="$$",
                average_cost_per_person=28.0,
                dietary_options=["vegetarian", "vegan", "gluten-free"],
                reservations_required=False,
                distance_km=1.5
            ),
            Restaurant(
                name=f"{destination} Street Food Market",
                cuisine="international",
                location=f"Market Square, {destination}",
                description="Vibrant food market with diverse international cuisines",
                rating=4.4,
                price_range="$",
                average_cost_per_person=15.0,
                dietary_options=["vegetarian", "vegan", "halal"],
                reservations_required=False,
                distance_km=0.5
            ),
            Restaurant(
                name=f"Le Gourmet {destination}",
                cuisine="french",
                location=f"Historic Center, {destination}",
                description="Fine dining French restaurant with Michelin-star experience",
                rating=4.9,
                price_range="$$$$",
                average_cost_per_person=120.0,
                dietary_options=["vegetarian"],
                reservations_required=True,
                distance_km=1.8
            ),
            Restaurant(
                name=f"Taco Fiesta",
                cuisine="mexican",
                location=f"Beach District, {destination}",
                description="Casual Mexican eatery with authentic tacos and margaritas",
                rating=4.3,
                price_range="$",
                average_cost_per_person=20.0,
                dietary_options=["vegetarian", "vegan", "gluten-free"],
                reservations_required=False,
                distance_km=3.2
            ),
            Restaurant(
                name=f"{destination} BBQ House",
                cuisine="american",
                location=f"Riverside, {destination}",
                description="American steakhouse with premium cuts and craft cocktails",
                rating=4.5,
                price_range="$$$",
                average_cost_per_person=70.0,
                dietary_options=["gluten-free"],
                reservations_required=True,
                distance_km=2.5
            )
        ]
        
        # Filter by cuisine if specified
        if cuisines:
            all_restaurants = [
                r for r in all_restaurants 
                if r.cuisine in cuisines
            ]
        
        # Filter by dietary restrictions if specified
        if dietary_restrictions:
            all_restaurants = [
                r for r in all_restaurants
                if any(diet in r.dietary_options for diet in dietary_restrictions)
            ]
        
        # Filter by price range if specified
        if price_range:
            all_restaurants = [
                r for r in all_restaurants
                if r.price_range == price_range
            ]
        
        return all_restaurants[:max_results]
    
    def get_top_restaurants(
        self,
        restaurants: List[Restaurant],
        count: int = 5
    ) -> List[Restaurant]:
        """Get top-rated restaurants
        
        Args:
            restaurants: List of restaurants to choose from
            count: Number of top restaurants to return
        
        Returns:
            List of top-rated Restaurant objects
        """
        sorted_restaurants = sorted(
            restaurants, 
            key=lambda r: r.rating, 
            reverse=True
        )
        return sorted_restaurants[:count]
    
    def get_budget_friendly_options(
        self,
        restaurants: List[Restaurant],
        max_budget_per_person: float
    ) -> List[Restaurant]:
        """Filter restaurants within budget
        
        Args:
            restaurants: List of restaurants to filter
            max_budget_per_person: Maximum budget per person
        
        Returns:
            List of restaurants within budget
        """
        return [
            r for r in restaurants
            if r.average_cost_per_person <= max_budget_per_person
        ]
    
    def get_nearby_restaurants(
        self,
        restaurants: List[Restaurant],
        max_distance_km: float = 2.0
    ) -> List[Restaurant]:
        """Filter restaurants by distance
        
        Args:
            restaurants: List of restaurants to filter
            max_distance_km: Maximum distance in kilometers
        
        Returns:
            List of nearby restaurants
        """
        return [
            r for r in restaurants
            if r.distance_km <= max_distance_km
        ]
    
    def calculate_dining_cost(
        self,
        restaurants: List[Restaurant],
        num_people: int = 1
    ) -> float:
        """Calculate total dining cost for selected restaurants
        
        Args:
            restaurants: List of selected restaurants
            num_people: Number of people dining
        
        Returns:
            Total estimated cost
        """
        return sum(r.average_cost_per_person * num_people for r in restaurants)
    
    def get_recommendations_by_meal_type(
        self,
        destination: str,
        meal_type: str,  # "breakfast", "lunch", "dinner"
        preferences: Optional[Dict[str, Any]] = None
    ) -> List[Restaurant]:
        """Get restaurant recommendations for specific meal type
        
        Args:
            destination: City or location
            meal_type: Type of meal (breakfast, lunch, dinner)
            preferences: User preferences (cuisine, dietary, budget)
        
        Returns:
            List of recommended restaurants
        """
        preferences = preferences or {}
        
        # Adjust search based on meal type
        if meal_type == "breakfast":
            cuisines = preferences.get("cuisines", ["american", "french"])
        elif meal_type == "lunch":
            cuisines = preferences.get("cuisines", None)
        else:  # dinner
            cuisines = preferences.get("cuisines", None)
        
        restaurants = self.discover_restaurants(
            destination=destination,
            cuisines=cuisines,
            dietary_restrictions=preferences.get("dietary_restrictions"),
            price_range=preferences.get("price_range")
        )
        
        return self.get_top_restaurants(restaurants, count=3)
    
    def create_dining_itinerary(
        self,
        destination: str,
        num_days: int,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Restaurant]]:
        """Create a complete dining itinerary
        
        Args:
            destination: City or location
            num_days: Number of days
            preferences: User preferences
        
        Returns:
            Dictionary with day-wise restaurant recommendations
        """
        itinerary = {}
        meal_types = ["breakfast", "lunch", "dinner"]
        
        for day in range(1, num_days + 1):
            day_key = f"Day {day}"
            itinerary[day_key] = {}
            
            for meal_type in meal_types:
                recommendations = self.get_recommendations_by_meal_type(
                    destination=destination,
                    meal_type=meal_type,
                    preferences=preferences
                )
                itinerary[day_key][meal_type] = recommendations[:1]  # One per meal
        
        return itinerary
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "RestaurantAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
