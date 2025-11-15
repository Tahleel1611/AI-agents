# SmartTravel AI - Multi-Agent Travel Concierge

## Overview

SmartTravel AI is an advanced AI-powered travel planning system that leverages multiple specialized agents to provide comprehensive travel recommendations and itineraries. Built with Google's Gemini API, this system coordinates intelligent agents to handle flights, accommodations, attractions, and complete travel planning.

## Features

- **Multi-Agent Architecture**: Specialized agents for different travel aspects
- **Intelligent Itinerary Generation**: Creates personalized travel plans
- **Flight Recommendations**: Searches and analyzes flight options
- **Accommodation Suggestions**: Recommends hotels and lodging
- **Attraction Discovery**: Finds local attractions and activities
- **Budget Optimization**: Helps plan within budget constraints
- **Gemini AI Integration**: Uses advanced language models for recommendations

## Project Structure

```
smart travel/
├── __init__.py              # Package initialization
├── config.py                # Configuration management
├── agents/                  # Agent modules
│   ├── __init__.py
│   ├── concierge.py        # Main orchestration agent
│   ├── flight_agent.py     # Flight search agent
│   ├── hotel_agent.py      # Accommodation agent
│   ├── attraction_agent.py # Local attractions agent
│   └── itinerary_agent.py  # Itinerary planning agent
├── utils/                   # Utility functions
│   └── helpers.py
├── tests/                   # Test suite
│   └── test_agents.py
└── requirements.txt         # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-agents.git
cd AI-agents/smarttravel
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export GEMINI_API_KEY="your-api-key-here"
export DEBUG="True"  # Optional, for development
```

## Usage

```python
from smarttravel import TravelConcierge, Config
from smarttravel.agents.concierge import TravelRequest

# Initialize the travel concierge
concierge = TravelConcierge(config=Config())

# Create a travel request
request = TravelRequest(
    destination="Paris",
    start_date="2024-06-01",
    end_date="2024-06-07",
    budget=5000,
    travelers=2,
    preferences={"type": "cultural", "pace": "moderate"}
)

# Process the request and get an itinerary
itinerary = concierge.process_request(request)
```

## API Keys Required

- **GEMINI_API_KEY**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **SKYSCANNER_API_KEY**: (Optional) Flight searches
- **BOOKING_COM_API_KEY**: (Optional) Hotel recommendations
- **GOOGLE_MAPS_API_KEY**: (Optional) Location-based services

## Technologies

- Python 3.12+
- Google Gemini API
- Multi-agent architecture
- Async/await for concurrent operations
- Type hints for code clarity

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Complete flight agent implementation
- [ ] Implement hotel recommendations
- [ ] Add attraction discovery
- [ ] Deploy to cloud platform
- [ ] Create web UI
- [ ] Add mobile app support

## Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ by SmartTravel AI Team**
