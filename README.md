# 🌍 TravelBuddy

### Autonomous Multi-Agent AI Travel Orchestrator

TravelBuddy is a production-grade multi-agent travel planning platform that leverages specialized AI agents to autonomously research, validate, and optimize travel itineraries in real time.

Unlike conventional chatbot-based travel assistants, TravelBuddy employs an Agentic Orchestration Engine that coordinates multiple domain-specific agents working in parallel. The result is faster decision-making, better recommendations, transparent pricing intelligence, and personalized travel planning.

---

## ✨ Key Features

### 🤖 Multi-Agent Intelligence

TravelBuddy distributes tasks across specialized AI agents rather than relying on a single monolithic model.

### ✈️ Real-Time Travel Discovery

Compare flights, accommodations, and transportation options across multiple providers to identify the best value opportunities.

### 🧠 Sentiment-Validated Recommendations

Destinations and attractions are validated using travel reviews, social content, and vlog-based sentiment analysis.

### 💰 Automated Cost Optimization

TravelBuddy continuously evaluates cost-efficiency and highlights price discrepancies across booking platforms.

### 🚆 Multi-Modal Transit Planning

Combines air travel, rail networks, and local transportation into a unified itinerary.

### 🇮🇳 INR-First Cost Analysis

All financial calculations and comparisons are optimized for Indian travelers with pricing displayed in INR (₹).

### ⚡ High-Speed Agent Execution

Powered by Groq LPUs and asynchronous parallel processing for near real-time response generation.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   User Interface     │
                    │      Streamlit       │
                    └──────────┬───────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │ Master Synthesis Engine      │
                │ Agent Orchestration Layer    │
                └──────────┬───────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Flight      │    │ Rail        │    │ Accommodation│
│ Broker      │    │ Transit     │    │ Broker       │
│ Agent       │    │ Agent       │    │ Agent        │
└─────────────┘    └─────────────┘    └─────────────┘

      ┌────────────────────┬────────────────────┐
                           │
                           ▼
                 ┌──────────────────┐
                 │ Social Sentiment │
                 │ Agent            │
                 └──────────────────┘
```

---

# 🤖 Agent Ecosystem

## ✈️ Flight Broker Agent

Responsible for discovering and evaluating flight options.

**Capabilities**

* Multi-provider search
* Price anomaly detection
* Fare comparison
* Route optimization
* Cost-performance analysis

**Data Sources**

* Google Flights
* Skyscanner
* Kayak
* Airline booking portals

---

## 🚆 Rail Transit Agent

Analyzes land transportation alternatives.

**Capabilities**

* Rail route planning
* Transit optimization
* Sustainability scoring
* Schedule evaluation

**Supported Networks**

* Vande Bharat Express
* Rajdhani Express
* Indian Railways
* EuroRail Networks

---

## 🏨 Accommodation Broker Agent

Performs accommodation cost-benefit analysis.

**Capabilities**

* Hotel vs Airbnb comparison
* Budget optimization
* Location scoring
* Amenity analysis
* Stay quality evaluation

---

## 📈 Social Sentiment Agent

Validates recommendations through public traveler experiences.

**Capabilities**

* Travel review analysis
* Vlog sentiment extraction
* Hidden-gem verification
* Tourist trap detection
* Experience scoring

---

## 🧩 Master Synthesis Engine

The central orchestration layer responsible for:

* Agent coordination
* Result aggregation
* Data cleaning
* Conflict resolution
* Final itinerary generation
* Booking link compilation

---

# 📊 Market Intelligence Layer

TravelBuddy acts as an automated travel market analyst.

### Real-Time Price Discovery

Continuously identifies pricing discrepancies across platforms.

### Opportunity Detection

Flags unusually low fares and accommodation deals.

### Cost Transparency

Provides side-by-side comparison of competing options.

### Smart Recommendations

Balances cost, convenience, traveler sentiment, and travel duration.

---

# 🛠️ Technology Stack

| Layer              | Technology               |
| ------------------ | ------------------------ |
| LLM Engine         | Groq LPU                 |
| Model              | Llama 3.3 70B            |
| Backend            | Python                   |
| Concurrency        | Asyncio                  |
| Frontend           | Streamlit                |
| Orchestration      | Multi-Agent Architecture |
| Configuration      | Environment Variables    |
| Secrets Management | .env Isolation           |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/prabalvarshney21/travel-planner-agents.git

cd travel-planner-agents
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

The application will launch locally and provide an interactive AI-powered travel planning experience through the Streamlit interface.

---

# 🔒 Security

TravelBuddy follows secure development practices:

* API keys stored via environment variables
* No hardcoded credentials
* Secret isolation through `.env`
* Modular agent architecture
* Secure configuration management

---

# 🎯 Use Cases

### Solo Travelers

Generate optimized itineraries with budget awareness.

### Business Travelers

Balance cost, convenience, and travel efficiency.

### Family Vacations

Compare accommodations, transportation, and attractions.

### Backpackers

Discover hidden gems and low-cost travel opportunities.

### International Travel

Evaluate flights, rail options, stays, and local experiences across multiple regions.

---

# 🔮 Future Roadmap

* Real-time booking execution
* Dynamic trip re-planning
* Weather-aware itinerary adaptation
* Multi-currency optimization
* Voice-enabled travel assistant
* Mobile application support
* Autonomous booking agents
* Predictive airfare forecasting

---

# 👨‍💻 Author

Prabal Varshney

Mechanical Engineering
Aligarh Muslim University

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub. Contributions, suggestions, and feature requests are always welcome.
