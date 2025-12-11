#!/usr/bin/env python3
"""
SmartTravel AI - Streamlit Web UI
User-friendly web interface for SmartTravel AI travel planning
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import json

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="SmartTravel AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .cost-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🤖 SmartTravel AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Your intelligent multi-agent travel concierge</p>", unsafe_allow_html=True)

# Sidebar  - Trip Planning Form
with st.sidebar:
    st.header("📋 Plan Your Trip")
    
    destination = st.text_input("Destination", placeholder="e.g., Paris, Tokyo, New York")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() + timedelta(days=7),
            min_value=datetime.now().date()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now() + timedelta(days=10),
            min_value=datetime.now().date()
        )
    
    origin = st.text_input("Origin (Optional)", placeholder="e.g., Mumbai, Delhi")
    
    budget = st.number_input(
        "Budget (INR)",
        min_value=0,
        max_value=10000000,
        value=50000,
        step=5000
    )
    
    travelers = st.number_input(
        "Number of Travelers",
        min_value=1,
        max_value=20,
        value=1
    )
    
    st.subheader("🎯 Preferences")
    attraction_types = st.multiselect(
        "Attraction Types",
        ["Museums", "Landmarks", "Nature", "Food & Dining", "Shopping", "Adventure", "Cultural", "Nightlife"],
        default=["Landmarks", "Food & Dining"]
    )
    
    plan_button = st.button("🚀 Plan My Trip", use_container_width=True)

# Main content area
if plan_button:
    if not destination:
        st.error("❌ Please enter a destination")
    elif end_date <= start_date:
        st.error("❌ End date must be after start date")
    else:
        with st.spinner("🤖 Our AI agents are planning your perfect trip...  "):
            try:
                # Prepare request payload
                payload = {
                    "destination": destination,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "origin": origin if origin else None,
                    "budget": float(budget),
                    "travelers": int(travelers),
                    "preferences": {
                        "attraction_types": attraction_types
                    }
                }
                
                # Call API
                response = requests.post(
                    f"{API_BASE_URL}/plan_trip",
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Success message
                    st.success(f"✅ {result.get('message', 'Trip plan generated successfully!')}")
                    
                    # Display total cost
                    st.markdown(f"""
                    <div class="cost-box">
                        <h2 style="margin: 0;">💰 Total Estimated Cost</h2>
                        <h1 style="color: #1f77b4; margin: 0.5rem 0;">₹{result['total_estimated_cost']:,.2f}</h1>
                        <p style="margin: 0;">For {result['duration_days']} days in {result['destination']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tabs for different sections
                    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Flights", "🏨 Accommodations", "🗺️ Attractions", "📅 Daily Schedule"])
                    
                    with tab1:
                        st.subheader("Flight Options")
                        if result.get('flights'):
                            for idx, flight in enumerate(result['flights'][:5], 1):
                                with st.expander(f"Option {idx}: {flight.get('airline', 'N/A')} - ₹{flight.get('price', 0):,.2f}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"**Departure:** {flight.get('departure', 'N/A')}")
                                    with col2:
                                        st.write(f"**Arrival:** {flight.get('arrival', 'N/A')}")
                        else:
                            st.info("No flight information available. Add an origin city to see flight options.")
                    
                    with tab2:
                        st.subheader("Recommended Accommodations")
                        if result.get('accommodations'):
                            for hotel in result['accommodations'][:5]:
                                with st.expander(f"{hotel.get('name', 'N/A')} - ₹{hotel.get('price_per_night', 0):,.2f}/night"):
                                    st.write(f"**Location:** {hotel.get('location', 'N/A')}")
                                    st.write(f"**Rating:** {'⭐' * int(hotel.get('rating', 0))} ({hotel.get('rating', 'N/A')})")
                        else:
                            st.info("No accommodation information available.")
                    
                    with tab3:
                        st.subheader("Top Attractions")
                        if result.get('attractions'):
                            for attraction in result['attractions']:
                                with st.expander(f"{attraction.get('name', 'N/A')} ({attraction.get('category', 'N/A')})"):
                                    st.write(f"**Description:** {attraction.get('description', 'N/A')}")
                                    price = attraction.get('price', 0)
                                    if price:
                                        st.write(f"**Entry Fee:** ₹{price:,.2f}")
                                    else:
                                        st.write("**Entry:** Free")
                        else:
                            st.info("No attraction information available.")
                    
                    with tab4:
                        st.subheader("Daily Itinerary")
                        if result.get('daily_schedule'):
                            for day in result['daily_schedule']:
                                with st.expander(f"📅 Day {day.get('day', 'N/A')} - {day.get('date', 'N/A')}"):
                                    activities = day.get('activities', [])
                                    if activities:
                                        for activity in activities:
                                            st.write(f"• {activity}")
                                    else:
                                        st.write("No specific activities planned for this day.")
                        else:
                            st.info("No daily schedule available.")
                    
                    # Download button for the itinerary
                    st.download_button(
                        label="📥 Download Itinerary (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name=f"smarttravel_{destination}_{start_date}.json",
                        mime="application/json"
                    )
                    
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error occurred')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the API server. Make sure the API is running on http://localhost:8000")
                st.info("💡 Run the API with: `python api.py` or `uvicorn api:app`")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The trip planning is taking longer than expected.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
else:
    # Welcome message
    st.info("👈 Fill in the form on the left to start planning your trip!")
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 Multi-Agent AI
        Our intelligent agents work together to create the perfect itinerary
        """)
    
    with col2:
        st.markdown("""
        ### 🌤️ Weather-Aware
        Real-time weather data ensures optimal activity timing
        """)
    
    with col3:
        st.markdown("""
        ### 💰 Budget Optimized
        Smart cost allocation across all trip components
        """)
    
    # Example trips
    st.subheader("✨ Popular Destinations")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400", caption="Paris")
    with col2:
        st.image("https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400", caption="Tokyo")
    with col3:
        st.image("https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=400", caption="Goa")
    with col4:
        st.image("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400", caption="Dubai")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Powered by SmartTravel AI | Multi-Agent System with Google Gemini</p>",
    unsafe_allow_html=True
)
