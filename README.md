🌍 TravelBuddy | Next-Gen AI Travel Orchestration
TravelBuddy is a production-grade, autonomous travel planning engine that moves beyond simple itinerary generation. By leveraging a 5-Agent Multi-Agent Orchestration architecture, TravelBuddy compares global market pricing, synthesizes social sentiment from travel vlogs and reviews, and synchronizes cross-modal transit logistics (Flights + Trains) into a single, high-fidelity itinerary.

🚀 The Multi-Agent Ecosystem
Unlike standard LLM chatbots, TravelBuddy delegates complex tasks to specialized agents running concurrently:

Flight Broker Agent: Scrapes and filters multi-provider data to find the lowest market rates.

Rail Transit Agent: Evaluates high-speed rail connectivity, ensuring seamless land-based travel options.

Accommodation Broker: Aggregates top-rated Hotels and Airbnbs to optimize cost-per-stay.

Social Sentiment Agent: Parses real-time data from YouTube travel vlogs, Reddit, and Google Reviews to identify "hidden gem" local spots.

Master Synthesis Agent: Compiles all agent outputs into a structured, executable travel roadmap with direct booking deep-links.

📊 Key Features
Global Market Price Broker: Real-time side-by-side pricing comparisons of Skyscanner, Kayak, Google Flights, Airbnb, and Booking.com.

Social Sentiment Engine: Doesn't just find locations—it validates them against crowd-sourced sentiment (vlogs/reviews) to ensure your "hidden gems" are actually worth visiting.

Telemetry Radar: A dedicated backend diagnostic tab for developers to monitor the "Proof of Work" of every agent in real-time.

Floating AI Companion: A production-grade persistent chat interface for immediate, context-aware travel support.

🛠️ Technology Stack
Inference Engine: Groq LPU Hardware Acceleration (llama-3.3-70b-versatile).

Concurrency: Asynchronous asyncio parallel tasking (Flight + Train + Hotel + Sentiment agents execute simultaneously).

Frontend: Production-grade Streamlit with custom CSS "Startup UI" branding.

Deployment Ready: Secure environment isolation, automated pricing matrices, and state-persistent UI.

📦 Setup & Deployment
1. Clone the repository
Bash
git clone https://github.com/prabalvarshney21/travel-planner-agents.git
cd travel-planner-agents
2. Configure Environment
Create a .env file in the root directory. Ensure this is never committed to Git.

Plaintext
GROQ_API_KEY=your_groq_api_key_here
3. Install Dependencies
Bash
python -m pip install -r requirements.txt
4. Run the Engine
Bash
streamlit run app.py
🛡️ Security & Privacy
TravelBuddy is built with a Security-First mindset:

Credential Isolation: All API keys are managed via local .env files, protected by a strictly configured .gitignore.

Data Minimization: No PII (Personally Identifiable Information) or itinerary history is stored in persistent databases; session state is purged upon application restart.
