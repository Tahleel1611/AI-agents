"""Disruption Agent - Monitors and handles travel disruptions

Specialized agent for detecting travel disruptions (flight cancellations, delays,
weather events, etc.) and generating revised itineraries.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class DisruptionType(Enum):
    """Types of travel disruptions"""
    FLIGHT_CANCELLED = "flight_cancelled"
    FLIGHT_DELAYED = "flight_delayed"
    SEVERE_WEATHER = "severe_weather"
    HOTEL_UNAVAILABLE = "hotel_unavailable"
    ATTRACTION_CLOSED = "attraction_closed"
    TRANSPORTATION_ISSUE = "transportation_issue"
    OTHER = "other"


class DisruptionSeverity(Enum):
    """Severity levels for disruptions"""
    LOW = "low"          # Minor inconvenience, easy workaround
    MEDIUM = "medium"    # Requires replanning, moderate impact
    HIGH = "high"        # Significant impact, major replanning needed
    CRITICAL = "critical" # Trip-ending issue, immediate action required


@dataclass
class Disruption:
    """Data class for a single disruption"""
    disruption_type: DisruptionType
    severity: DisruptionSeverity
    affected_date: str
    description: str
    affected_components: List[str] = field(default_factory=list)  # e.g., ["flight", "hotel"]
    detected_at: datetime = field(default_factory=datetime.now)
    

@dataclass
class DisruptionReport:
    """Complete report of all disruptions found"""
    disruptions: List[Disruption] = field(default_factory=list)
    risk_score: float = 0.0  # 0-100 scale
    recommendations: List[str] = field(default_factory=list)
    requires_replanning: bool = False
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class RevisedItinerary:
    """Revised itinerary after handling disruptions"""
    original_itinerary: Dict[str, Any]
    disruptions_addressed: List[Disruption]
    changes: List[Dict[str, Any]] = field(default_factory=list)
    new_flights: List[Dict] = field(default_factory=list)
    new_accommodations: List[Dict] = field(default_factory=list)
    new_daily_schedule: List[Dict] = field(default_factory=list)
    estimated_additional_cost: float = 0.0
    revision_notes: str = ""
    revised_at: datetime = field(default_factory=datetime.now)


class DisruptionAgent:
    """Agent specialized in detecting and handling travel disruptions
    
    Monitors itineraries for potential disruptions and generates revised plans
    when issues are detected.
    """
    
    def __init__(self, config=None):
        """Initialize the Disruption Agent
        
        Args:
            config: Configuration object with API keys and settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("DisruptionAgent initialized")
    
    def detect_disruptions(
        self,
        itinerary: Dict[str, Any],
        live_data: Optional[Dict[str, Any]] = None
    ) -> DisruptionReport:
        """Detect potential disruptions in an itinerary
        
        Args:
            itinerary: Travel itinerary to check
            live_data: Optional real-time data (flight status, weather, etc.)
        
        Returns:
            DisruptionReport with detected issues
        """
        logger.info(f"Checking itinerary for {itinerary.get('destination')} for disruptions")
        
        disruptions = []
        
        # Mock implementation - in production, this would call external APIs
        # Check for flight issues
        if live_data and live_data.get("flight_cancelled"):
            disruptions.append(
                Disruption(
                    disruption_type=DisruptionType.FLIGHT_CANCELLED,
                    severity=DisruptionSeverity.HIGH,
                    affected_date=itinerary.get("start_date", ""),
                    description="Outbound flight has been cancelled",
                    affected_components=["flight", "day_1_activities"]
                )
            )
        
        if live_data and live_data.get("flight_delayed_hours", 0) > 3:
            delay_hours = live_data.get("flight_delayed_hours")
            disruptions.append(
                Disruption(
                    disruption_type=DisruptionType.FLIGHT_DELAYED,
                    severity=DisruptionSeverity.MEDIUM,
                    affected_date=itinerary.get("start_date", ""),
                    description=f"Flight delayed by {delay_hours} hours",
                    affected_components=["flight", "day_1_activities"]
                )
            )
        
        # Check for weather issues
        if live_data and live_data.get("severe_weather"):
            weather_info = live_data.get("severe_weather")
            disruptions.append(
                Disruption(
                    disruption_type=DisruptionType.SEVERE_WEATHER,
                    severity=DisruptionSeverity.MEDIUM,
                    affected_date=weather_info.get("date", ""),
                    description=weather_info.get("description", "Severe weather expected"),
                    affected_components=["outdoor_activities"]
                )
            )
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(disruptions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(disruptions)
        
        # Determine if replanning is required
        requires_replanning = any(
            d.severity in [DisruptionSeverity.HIGH, DisruptionSeverity.CRITICAL]
            for d in disruptions
        )
        
        return DisruptionReport(
            disruptions=disruptions,
            risk_score=risk_score,
            recommendations=recommendations,
            requires_replanning=requires_replanning
        )
    
    def generate_revised_itinerary(
        self,
        original_itinerary: Dict[str, Any],
        disruption_report: DisruptionReport
    ) -> RevisedItinerary:
        """Generate a revised itinerary to handle disruptions
        
        Args:
            original_itinerary: Original travel itinerary
            disruption_report: Report of detected disruptions
        
        Returns:
            RevisedItinerary with changes and alternatives
        """
        logger.info("Generating revised itinerary")
        
        changes = []
        new_flights = []
        new_accommodations = []
        new_daily_schedule = []
        additional_cost = 0.0
        notes = []
        
        for disruption in disruption_report.disruptions:
            if disruption.disruption_type == DisruptionType.FLIGHT_CANCELLED:
                # Mock: Generate alternative flights
                new_flights = self._find_alternative_flights(
                    original_itinerary.get("flights", [])
                )
                changes.append({
                    "type": "flight_replacement",
                    "description": "Booked alternative flight",
                    "affected_date": disruption.affected_date
                })
                additional_cost += 200.0  # Mock rebooking fee
                notes.append("Flight rebooked to next available departure")
            
            elif disruption.disruption_type == DisruptionType.FLIGHT_DELAYED:
                # Adjust day 1 schedule
                new_daily_schedule = self._adjust_schedule_for_delay(
                    original_itinerary.get("daily_schedule", [])
                )
                changes.append({
                    "type": "schedule_adjustment",
                    "description": "Day 1 activities rescheduled",
                    "affected_date": disruption.affected_date
                })
                notes.append("First day activities postponed to accommodate delay")
            
            elif disruption.disruption_type == DisruptionType.SEVERE_WEATHER:
                # Replace outdoor activities with indoor alternatives
                new_daily_schedule = self._replace_with_indoor_activities(
                    original_itinerary.get("daily_schedule", []),
                    disruption.affected_date
                )
                changes.append({
                    "type": "activity_replacement",
                    "description": "Outdoor activities replaced with indoor alternatives",
                    "affected_date": disruption.affected_date
                })
                notes.append("Moved outdoor activities to indoor venues due to weather")
        
        revision_notes = " | ".join(notes) if notes else "Minor adjustments made"
        
        return RevisedItinerary(
            original_itinerary=original_itinerary,
            disruptions_addressed=disruption_report.disruptions,
            changes=changes,
            new_flights=new_flights,
            new_accommodations=new_accommodations,
            new_daily_schedule=new_daily_schedule,
            estimated_additional_cost=additional_cost,
            revision_notes=revision_notes
        )
    
    def _calculate_risk_score(self, disruptions: List[Disruption]) -> float:
        """Calculate overall risk score from disruptions
        
        Args:
            disruptions: List of detected disruptions
        
        Returns:
            Risk score from 0-100
        """
        if not disruptions:
            return 0.0
        
        severity_weights = {
            DisruptionSeverity.LOW: 10,
            DisruptionSeverity.MEDIUM: 30,
            DisruptionSeverity.HIGH: 60,
            DisruptionSeverity.CRITICAL: 100
        }
        
        total_score = sum(
            severity_weights.get(d.severity, 0)
            for d in disruptions
        )
        
        # Cap at 100
        return min(total_score, 100.0)
    
    def _generate_recommendations(self, disruptions: List[Disruption]) -> List[str]:
        """Generate actionable recommendations based on disruptions
        
        Args:
            disruptions: List of detected disruptions
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        for disruption in disruptions:
            if disruption.disruption_type == DisruptionType.FLIGHT_CANCELLED:
                recommendations.append(
                    "Contact airline immediately for rebooking options"
                )
                recommendations.append(
                    "Consider flexible accommodation if arrival is delayed"
                )
            
            elif disruption.disruption_type == DisruptionType.SEVERE_WEATHER:
                recommendations.append(
                    "Have backup indoor activities planned"
                )
                recommendations.append(
                    "Check local weather alerts regularly"
                )
            
            elif disruption.disruption_type == DisruptionType.ATTRACTION_CLOSED:
                recommendations.append(
                    "Research alternative attractions in the area"
                )
        
        return recommendations
    
    def _find_alternative_flights(self, original_flights: List[Dict]) -> List[Dict]:
        """Find alternative flights (mock implementation)
        
        Args:
            original_flights: List of cancelled/unavailable flights
        
        Returns:
            List of alternative flight options
        """
        # Mock implementation
        return [
            {
                "airline": "Alternative Airways",
                "departure": "2024-06-01 14:00",
                "arrival": "2024-06-01 16:30",
                "price": 450.0,
                "note": "Rebooked flight"
            }
        ]
    
    def _adjust_schedule_for_delay(self, daily_schedule: List[Dict]) -> List[Dict]:
        """Adjust daily schedule to accommodate flight delays
        
        Args:
            daily_schedule: Original daily schedule
        
        Returns:
            Adjusted schedule
        """
        # Mock implementation - shift day 1 activities
        adjusted = daily_schedule.copy()
        if adjusted and len(adjusted) > 0:
            # Remove early morning activities from day 1
            adjusted[0]["activities"] = adjusted[0].get("activities", [])[1:]
        return adjusted
    
    def _replace_with_indoor_activities(
        self,
        daily_schedule: List[Dict],
        affected_date: str
    ) -> List[Dict]:
        """Replace outdoor activities with indoor alternatives
        
        Args:
            daily_schedule: Original daily schedule
            affected_date: Date affected by weather
        
        Returns:
            Modified schedule with indoor activities
        """
        # Mock implementation
        adjusted = daily_schedule.copy()
        for day in adjusted:
            if day.get("date") == affected_date:
                # Replace with indoor activities
                day["activities"] = [
                    "Visit local museum",
                    "Explore art gallery",
                    "Indoor market tour",
                    "Cooking class"
                ]
                day["weather_note"] = "Schedule adjusted for indoor activities"
        return adjusted
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "DisruptionAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat()
        
