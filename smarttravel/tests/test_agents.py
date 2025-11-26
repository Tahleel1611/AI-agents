"""Tests for SmartTravel AI agents"""

import pytest
from datetime import datetime

from smarttravel.agents.flight_agent import FlightAgent, FlightOption
from smarttravel.agents.hotel_agent import HotelAgent, HotelOption
from smarttravel.agents.attraction_agent import AttractionAgent, Attraction
from smarttravel.agents.itinerary_agent import ItineraryAgent
from smarttravel.agents.concierge import TravelConcierge, TravelRequest


class TestFlightAgent:
    """Tests for FlightAgent"""
    
    def test_init(self):
        """Test FlightAgent initialization"""
        agent = FlightAgent()
        assert agent.initialized_at is not None
    
    def test_search_flights(self):
        """Test flight search functionality"""
        agent = FlightAgent()
        flights = agent.search_flights("NYC", "Paris", "2024-06-01")
        assert len(flights) == 2
        assert all(isinstance(f, FlightOption) for f in flights)
    
    def test_get_best_flight_by_price(self):
        """Test getting best flight by price"""
        agent = FlightAgent()
        flights = agent.search_flights("NYC", "Paris", "2024-06-01")
        best = agent.get_best_flight(flights, "price")
        assert best is not None
        assert best.price == min(f.price for f in flights)
    
    def test_get_best_flight_empty_list(self):
        """Test getting best flight from empty list"""
        agent = FlightAgent()
        best = agent.get_best_flight([], "price")
        assert best is None


class TestHotelAgent:
    """Tests for HotelAgent"""
    
    def test_init(self):
        """Test HotelAgent initialization"""
        agent = HotelAgent()
        assert agent.initialized_at is not None
    
    def test_search_hotels(self):
        """Test hotel search functionality"""
        agent = HotelAgent()
        hotels = agent.search_hotels("Paris", "2024-06-01", "2024-06-07")
        assert len(hotels) == 3
        assert all(isinstance(h, HotelOption) for h in hotels)
    
    def test_calculate_total_cost(self):
        """Test total cost calculation"""
        agent = HotelAgent()
        hotel = HotelOption(
            name="Test Hotel",
            location="Test Location",
            star_rating=4,
            price_per_night=100.0,
            amenities=["WiFi"]
        )
        cost = agent.calculate_total_cost(hotel, nights=5, rooms=2)
        assert cost == 1000.0


class TestAttractionAgent:
    """Tests for AttractionAgent"""
    
    def test_init(self):
        """Test AttractionAgent initialization"""
        agent = AttractionAgent()
        assert agent.initialized_at is not None
    
    def test_discover_attractions(self):
        """Test attraction discovery"""
        agent = AttractionAgent()
        attractions = agent.discover_attractions("Paris")
        assert len(attractions) == 5
        assert all(isinstance(a, Attraction) for a in attractions)
    
    def test_discover_attractions_with_filter(self):
        """Test attraction discovery with category filter"""
        agent = AttractionAgent()
        attractions = agent.discover_attractions("Paris", categories=["museum"])
        assert len(attractions) == 1
        assert attractions[0].category == "museum"
    
    def test_calculate_activities_cost(self):
        """Test activities cost calculation"""
        agent = AttractionAgent()
        attractions = agent.discover_attractions("Paris")
        cost = agent.calculate_activities_cost(attractions)
        assert cost > 0


class TestItineraryAgent:
    """Tests for ItineraryAgent"""
    
    def test_init(self):
        """Test ItineraryAgent initialization"""
        agent = ItineraryAgent()
        assert agent.initialized_at is not None
    
    def test_create_itinerary(self):
        """Test itinerary creation"""
        agent = ItineraryAgent()
        itinerary = agent.create_itinerary("Paris", "2024-06-01", "2024-06-07")
        assert itinerary.destination == "Paris"
        assert len(itinerary.days) == 7
    
    def test_get_daily_summary(self):
        """Test daily summary retrieval"""
        agent = ItineraryAgent()
        itinerary = agent.create_itinerary("Paris", "2024-06-01", "2024-06-03")
        summary = agent.get_daily_summary(itinerary, 1)
        assert summary is not None
        assert "Day 1" in summary


class TestTravelConcierge:
    """Tests for TravelConcierge"""
    
    def test_init(self):
        """Test TravelConcierge initialization"""
        concierge = TravelConcierge()
        assert concierge.initialized_at is not None
        assert concierge.flight_agent is not None
        assert concierge.hotel_agent is not None
    
    def test_process_request(self):
        """Test processing a travel request"""
        concierge = TravelConcierge()
        request = TravelRequest(
            destination="Paris",
            start_date="2024-06-01",
            end_date="2024-06-07",
            origin="NYC",
            travelers=2
        )
        result = concierge.process_request(request)
        assert result.destination == "Paris"
        assert result.duration_days == 7
        assert len(result.flights) > 0
        assert len(result.accommodations) > 0
        assert result.total_estimated_cost > 0
    
    def test_calculate_duration(self):
        """Test duration calculation"""
        concierge = TravelConcierge()
        duration = concierge._calculate_duration("2024-06-01", "2024-06-07")
        assert duration == 7
    
    def test_get_status(self):
        """Test status retrieval"""
        concierge = TravelConcierge()
        status = concierge.get_status()
        assert status["status"] == "active"
        assert "agents" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
