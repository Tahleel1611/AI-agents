"""Itinerary Agent - Handles trip planning and scheduling

Specialized agent for creating comprehensive travel itineraries.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class DayPlan:
    """Data class for a single day's plan"""
    day_number: int
    date: str
    activities: List[Dict[str, Any]]
    notes: str = ""


@dataclass
class Itinerary:
    """Data class for complete itinerary"""
    destination: str
    start_date: str
    end_date: str
    days: List[DayPlan]
    total_budget: float = 0.0
    summary: str = ""


class ItineraryAgent:
    """Agent specialized in itinerary planning and scheduling
    
    Creates comprehensive day-by-day travel itineraries by coordinating
    flights, accommodations, and activities.
    """
    
    def __init__(self, config=None):
        """Initialize the Itinerary Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("ItineraryAgent initialized")
    
    def create_itinerary(
        self,
        destination: str,
        start_date: str,
        end_date: str,
        attractions: Optional[List[Any]] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Itinerary:
        """Create a complete travel itinerary
        
        Args:
            destination: Travel destination
            start_date: Trip start date (YYYY-MM-DD)
            end_date: Trip end date (YYYY-MM-DD)
            attractions: List of attractions to include
            preferences: User preferences for pacing and style
            
        Returns:
            Complete Itinerary object
        """
        logger.info(f"Creating itinerary for {destination}")
        
        # Calculate number of days
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end - start).days + 1
        
        # Generate day plans
        days = []
        attractions_list = attractions or []
        attractions_per_day = max(1, len(attractions_list) // num_days) if attractions_list else 2
        
        for i in range(num_days):
            current_date = start + timedelta(days=i)
            
            # Distribute attractions across days
            start_idx = i * attractions_per_day
            end_idx = start_idx + attractions_per_day
            day_attractions = attractions_list[start_idx:end_idx] if attractions_list else []
            
            activities = []
            
            # Morning activity
            activities.append({
                "time": "09:00",
                "type": "breakfast",
                "description": "Breakfast at hotel"
            })
            
            # Add attractions as activities
            hour = 10
            for attraction in day_attractions:
                attraction_name = getattr(attraction, 'name', str(attraction))
                activities.append({
                    "time": f"{hour:02d}:00",
                    "type": "attraction",
                    "description": f"Visit {attraction_name}"
                })
                hour += 3
            
            # Add default activities if no attractions
            if not day_attractions:
                activities.append({
                    "time": "10:00",
                    "type": "exploration",
                    "description": f"Explore {destination}"
                })
            
            # Evening activity
            activities.append({
                "time": "19:00",
                "type": "dinner",
                "description": "Dinner at local restaurant"
            })
            
            day_plan = DayPlan(
                day_number=i + 1,
                date=current_date.strftime("%Y-%m-%d"),
                activities=activities,
                notes=f"Day {i + 1} in {destination}"
            )
            days.append(day_plan)
        
        itinerary = Itinerary(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            days=days,
            summary=f"{num_days}-day trip to {destination}"
        )
        
        return itinerary
    
    def optimize_schedule(
        self,
        itinerary: Itinerary,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Itinerary:
        """Optimize an existing itinerary
        
        Args:
            itinerary: Existing itinerary to optimize
            constraints: Optimization constraints (budget, time, preferences)
            
        Returns:
            Optimized Itinerary object
        """
        logger.info("Optimizing itinerary schedule")
        # In production, this would apply ML/AI optimization
        return itinerary
    
    def add_activity(
        self,
        itinerary: Itinerary,
        day_number: int,
        activity: Dict[str, Any]
    ) -> Itinerary:
        """Add an activity to a specific day
        
        Args:
            itinerary: Itinerary to modify
            day_number: Day to add activity to (1-indexed)
            activity: Activity details
            
        Returns:
            Updated Itinerary object
        """
        if 1 <= day_number <= len(itinerary.days):
            itinerary.days[day_number - 1].activities.append(activity)
            # Sort by time
            itinerary.days[day_number - 1].activities.sort(
                key=lambda x: x.get("time", "00:00")
            )
        return itinerary
    
    def get_daily_summary(
        self,
        itinerary: Itinerary,
        day_number: int
    ) -> Optional[str]:
        """Get summary for a specific day
        
        Args:
            itinerary: Itinerary to query
            day_number: Day number (1-indexed)
            
        Returns:
            Summary string for the day, or None if day not found
        """
        if 1 <= day_number <= len(itinerary.days):
            day = itinerary.days[day_number - 1]
            activities = [a.get("description", "") for a in day.activities]
            return f"Day {day_number}: " + " → ".join(activities)
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "ItineraryAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        }
