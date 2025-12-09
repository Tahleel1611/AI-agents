# 🤖 AI-Agents

> Building intelligent, autonomous agents powered by cutting-edge AI models

A modern repository for developing and deploying AI agents using Google's Gemini API. This project demonstrates practical implementations of AI-driven automation, intelligent decision-making, and seamless integration with powerful language models.

---

## 🌟 What is SmartTravel AI?

**SmartTravel AI** is an intelligent multi-agent travel concierge that helps you plan perfect trips with real-time insights and budget optimization.

**Example:** "Plan a 5-day trip to Tokyo for ₹80,000 with weather-aware activities"
- 🌤️ **Weather Agent**: Checks live forecasts to recommend optimal timing
- 🗺️ **Itinerary Agent**: Crafts day-by-day plans with attractions, restaurants, and hotels  
- 💰 **Budget Optimizer**: Balances costs across accommodation, food, and activities
- ✈️ **Flight Agent**: Finds best travel options within your budget

### Architecture

SmartTravel uses a **multi-agent coordination system** where specialized agents collaborate:
1. **User Query** → Concierge receives travel request
2. **Weather Agent** → Fetches real-time weather data for destination
3. **Planner Agent** → Generates itinerary based on weather and preferences  
4. **Budget Optimizer** → Adjusts recommendations to meet spending limits
5. **Output** → Unified travel plan with all details

---

## 📦 Project Components

### `my_agent/`
**Generic AI Agent Framework**  
Core reusable agent architecture with Gemini API integration. Includes base agent classes, prompt management, and response handling.

### `smarttravel/`
**SmartTravel Travel Concierge**  
Multi-agent travel planning system with specialized agents:
- `agents/itinerary_agent.py` - Day-by-day trip planning
- `agents/flight_agent.py` - Flight search and booking recommendations
- `agents/hotel_agent.py` - Accommodation suggestions
- `agents/restaurant_agent.py` - Dining recommendations  
- `agents/attraction_agent.py` - Tourist attraction curation
- `agents/budget_optimizer_agent.py` - Cost optimization across trip components
- `agents/disruption_agent.py` - Handles travel disruptions and rescheduling
- `concierge.py` - Orchestrates all agents for unified travel planning

### `weather_agent/`
**Weather Intelligence Micro-Agent**  
Standalone weather data agent that provides forecasts, historical data, and weather-aware recommendations for travel planning.

### `main.py`
**Entry Point**  
Primary interface for SmartTravel AI. Supports interactive mode and direct query execution.

### `Makefile`
**Development Automation**  
Common tasks (install, lint, format, run, test) wrapped in simple commands.

---

## ✨ Features

- 🧠 **Intelligent Agents** - Autonomous AI agents capable of complex reasoning and task execution
- ⚡ **Gemini Integration** - Leverages Google's Gemini API for state-of-the-art natural language understanding  
- 🔧 **Modular Architecture** - Clean, extensible codebase designed for rapid development
- 🚀 **Production Ready** - Built with best practices for scalability and reliability
- 🌍 **Travel Intelligence** - Multi-agent system specialized for travel planning with real-time data
- 💵 **Budget Optimization** - Smart cost allocation across travel components

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+  
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Tahleel1611/AI-agents.git
cd AI-agents
```

2. **Set up virtual environment**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac  
source .venv/bin/activate
```

3. **Install dependencies**

```bash
make install
# Or manually:
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
# Create .env file in my_agent/ directory
echo GOOGLE_API_KEY="your_api_key_here" > my_agent/.env
echo GOOGLE_GENAI_USE_VERTEXAI=0 >> my_agent/.env
```

---

## 💻 Usage

### Run SmartTravel AI (Interactive Mode)

```bash
make run
# Or:
python main.py --interactive
```

### Run SmartTravel AI with Direct Query

```bash
make run-query QUERY="Plan a weekend trip to Paris under €1500"
# Or:
python main.py "Plan a weekend trip to Paris under €1500"
```

### Run Generic Agent Demo

```bash
make run-my-agent  
# Or:
cd my_agent && python agent.py
```

### Run Weather Agent Demo

```bash
cd weather_agent && python weather_agent.py
```

---

## 🛠️ Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install all dependencies from requirements.txt |
| `make run` | Launch SmartTravel AI in interactive mode |
| `make run-query QUERY="..."` | Run SmartTravel with specific query |
| `make run-my-agent` | Run generic agent demo |
| `make test` | Run pytest with coverage |
| `make lint` | Run linting (ruff + flake8 + mypy) |
| `make format` | Format code (black + ruff) |
| `make clean` | Remove build artifacts and caches |

---

## ⚙️ Configuration

### Environment Variables

| Variable | Location | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | `my_agent/.env` | **(required)** | Your Google Gemini API key |
| `GOOGLE_GENAI_USE_VERTEXAI` | `my_agent/.env` | `0` | Use Vertex AI (1) or standard Gemini API (0) |
| `MODEL_NAME` | `smarttravel/config.py` | `gemini-1.5-pro` | Gemini model to use |
| `DEFAULT_BUDGET` | `smarttravel/config.py` | `50000` | Default trip budget in INR |
| `MAX_TRIP_DAYS` | `smarttravel/config.py` | `14` | Maximum trip duration |

---

## 📁 Project Structure

```
AI-agents/
├── my_agent/              # Core generic agent implementation
│   ├── agent.py           # Main agent logic  
│   ├── .env               # Environment configuration (not tracked)
│   └── __init__.py
├── smarttravel/           # SmartTravel travel concierge
│   ├── agents/            # Specialized travel agents
│   │   ├── __init__.py
│   │   ├── itinerary_agent.py
│   │   ├── flight_agent.py
│   │   ├── hotel_agent.py
│   │   ├── restaurant_agent.py
│   │   ├── attraction_agent.py
│   │   ├── budget_optimizer_agent.py
│   │   └── disruption_agent.py
│   ├── tests/             # Unit and integration tests
│   ├── concierge.py       # Multi-agent orchestrator
│   ├── config.py          # Configuration management
│   ├── requirements.txt   # SmartTravel-specific dependencies
│   └── README.md          # SmartTravel documentation
├── weather_agent/         # Weather intelligence micro-agent
│   ├── weather_agent.py   # Weather data fetching and analysis
│   └── __init__.py
├── main.py                # Main entry point for SmartTravel AI
├── Makefile               # Development automation
├── .gitignore             # Git ignore rules  
├── README.md              # This file
└── requirements.txt       # Root project dependencies
```

---

## 🎯 Use Cases

### 1. Weekend Trip Planner  
*"Plan a 3-day romantic getaway to Goa for ₹25,000"*  
- Budget-conscious itinerary with beach activities
- Weather-aware scheduling (monsoon alerts, best beach days)
- Romantic restaurant and sunset spot recommendations

### 2. Multi-City Budget Travel
*"Plan a 10-day backpacking trip across Rajasthan for ₹40,000"*  
- Optimizes city sequence based on travel costs
- Balances budget across multiple destinations  
- Suggests hostels, street food, and free attractions

### 3. Weather-Aware Rescheduling
*"I'm in Manali and it's raining all week—suggest alternative activities"*  
- Disruption Agent monitors weather changes
- Recommends indoor attractions, cafes, and day trips  
- Adjusts itinerary in real-time

---

## 🔮 Future Work

- [ ] **Web UI Integration** - React/Next.js frontend for visual trip planning
- [ ] **Real-time Flight/Hotel APIs** - Direct booking integration (Amadeus, Skyscanner)
- [ ] **User Profile Memory** - Save preferences, past trips, and loyalty programs
- [ ] **RAG over Travel Docs** - Retrieval-augmented generation with Lonely Planet, travel blogs
- [ ] **Social Features** - Share itineraries, collaborative trip planning
- [ ] **Mobile App** - iOS/Android companion for on-the-go updates
- [ ] **Voice Interface** - Natural language trip planning via voice commands
- [ ] **Multi-language Support** - Expand beyond English for global travelers

---

## 🔒 Security

- **Never commit API keys or secrets** - Use `.env` files (already ignored by git)
- Rotate your API keys immediately if accidentally exposed  
- Review `.gitignore` to ensure sensitive files are excluded

---

## 🛠️ Development

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request

### Best Practices

- Keep your `.env` file private and never commit it
- Use meaningful commit messages  
- Write clean, documented code
- Test your agents thoroughly before deployment
- Run `make lint` and `make format` before committing

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Connect

Built by [@Tahleel1611](https://github.com/Tahleel1611)

⭐ Star this repo if you find it helpful!

**Note:** Remember to replace placeholder API keys with your actual credentials and keep them secure!
