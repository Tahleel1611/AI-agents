#!/usr/bin/env python3
"""
SmartTravel AI - FastAPI Backend
RESTful API wrapper around the SmartTravel multi-agent system
"""

import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uvicorn

# Add smarttravel to path
sys.path.insert(0, str(Path(__file__).parent / 'smarttravel'))

from smarttravel.agents.concierge import TravelConcierge, TravelRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SmartTravel AI API",
    description="Multi-agent AI travel concierge API powered by Google Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global concierge instance
concierge = None


class TripRequest(BaseModel):
    """Request model for trip planning"""
    destination: str = Field(..., description="Travel destination", min_length=1)
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    origin: Optional[str] = Field(None, description="Origin city/airport")
    budget: Optional[float] = Field(None, description="Budget in INR", gt=0)
    travelers: int = Field(1, description="Number of travelers", gt=0, le=20)
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Travel preferences")

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    @validator('end_date')
    def validate_end_after_start(cls, v, values):
        """Validate end date is after start date"""
        if 'start_date' in values:
            start = datetime.strptime(values['start_date'], '%Y-%m-%d')
            end = datetime.strptime(v, '%Y-%m-%d')
            if end <= start:
                raise ValueError('end_date must be after start_date')
        return v


class TripResponse(BaseModel):
    """Response model for trip planning"""
    destination: str
    duration_days: int
    flights: List[Dict[str, Any]]
    accommodations: List[Dict[str, Any]]
    attractions: List[Dict[str, Any]]
    daily_schedule: List[Dict[str, Any]]
    total_estimated_cost: float
    message: str = "Trip plan generated successfully"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the concierge on startup"""
    global concierge
    try:
        logger.info("Initializing SmartTravel AI Concierge...")
        concierge = TravelConcierge()
        logger.info("SmartTravel AI API is ready!")
    except Exception as e:
        logger.error(f"Failed to initialize concierge: {e}")
        raise


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SmartTravel AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if concierge else "unhealthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post(
    "/plan_trip",
    response_model=TripResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def plan_trip(request: TripRequest) -> TripResponse:
    """
    Plan a trip based on the provided parameters.
    
    - **destination**: Travel destination (required)
    - **start_date**: Trip start date in YYYY-MM-DD format (required)
    - **end_date**: Trip end date in YYYY-MM-DD format (required)
    - **origin**: Origin city/airport (optional)
    - **budget**: Budget in INR (optional)
    - **travelers**: Number of travelers (default: 1)
    - **preferences**: Travel preferences dict (optional)
    
    Returns a comprehensive travel itinerary with flights, hotels, attractions, and schedule.
    """
    if not concierge:
        logger.error("Concierge not initialized")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Travel concierge service unavailable"
        )
    
    try:
        logger.info(f"Processing trip request for {request.destination}")
        
        # Convert API request to internal TravelRequest
        travel_request = TravelRequest(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            origin=request.origin or "",
            budget=request.budget,
            preferences=request.preferences,
            travelers=request.travelers
        )
        
        # Process the request through the concierge
        itinerary = concierge.process_request(travel_request)
        
        # Convert internal itinerary to API response
        response = TripResponse(
            destination=itinerary.destination,
            duration_days=itinerary.duration_days,
            flights=itinerary.flights,
            accommodations=itinerary.accommodations,
            attractions=itinerary.attractions,
            daily_schedule=itinerary.daily_schedule,
            total_estimated_cost=itinerary.total_estimated_cost
        )
        
        logger.info(f"Successfully generated trip plan for {request.destination}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing trip request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate trip plan: {str(e)}"
        )


@app.get("/status")
async def get_status():
    """Get detailed status of the concierge and all agents"""
    if not concierge:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Concierge not initialized"
        )
    
    try:
        return concierge.get_status()
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
