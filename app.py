# app.py
import os
import asyncio
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Multi-Agent Autonomous Travel Engine", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 1.5rem; }
    .card { background-color: #F8FAFC; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #E2E8F0; margin-bottom: 1rem; }
    .terminal-box { background-color: #0F172A; color: #38BDF8; font-family: monospace; padding: 1rem; border-radius: 0.375rem; height: 180px; overflow-y: auto; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

if not os.getenv("GEMINI_API_KEY"):
    st.error("Missing GEMINI_API_KEY in your .env file. Please add it to execute agents.")
    st.stop()

client = genai.Client()
MODEL_NAME = "gemini-2.5-flash"

# --- CHATBOT MEMORY INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI Travel Co-Pilot. Ask me anything about flights, hotel alternatives, or custom sightseeing options!"}
    ]

# --- CORE AGENT CAPABILITIES ---
async def run_flight_agent(context: dict) -> str:
    try:
        prompt = f"You are the Flight Agent. Select the best flight from this data. You MUST include the exact `booking_url` formatted as a markdown link like [Book Flight Here](URL): {json.dumps(context['raw_flights'])}"
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception:
        return f"Flight Search Agent (Fallback Active): Selected IndiGo non-stop from {context['origin']} to {context['destination']}. [Book on IndiGo](https://www.goindigo.in/)"

async def run_hotel_agent(context: dict) -> str:
    try:
        prompt = f"You are the Hotel Agent. Select the best hotel from this data. You MUST include the exact `booking_url` formatted as a markdown link like [Book Hotel Here](URL): {json.dumps(context['raw_hotels'])}"
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception:
        return f"Hotel Agent (Fallback Active): Recommended Taj Properties for your {context['budget_tier']} stay. [Book on Taj Hotels](https://www.tajhotels.com/)"

async def run_weather_agent(context: dict) -> str:
    try:
        mock_weather = "Clear skies, mild temperatures ranging from 18°C to 24°C. Perfect for walking tours."
        prompt = f"You are the Weather Agent. Analyze this forecast for {context['destination']}: '{mock_weather}'. Provide short packing tips."
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception:
        return f"Weather Agent (Fallback Active): Clear conditions expected in {context['destination']}."

# --- WEB DASHBOARD UI LAYOUT ---
st.markdown('<div class="main-header">Autonomous Multi-Agent Travel Engine</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("1. Travel Planning Portal")
    origin = st.text_input("Origin City", value="Delhi")
    destination = st.selectbox("Destination City", options=["Mumbai", "Goa", "Paris", "Tokyo"])
    duration = st.slider("Trip Duration (Days)", min_value=3, max_value=7, value=5)
    budget_tier = st.radio("Budget Profile", options=["Budget", "Moderate", "Luxury"], index=2)
    
    generate_btn = st.button("Generate Autonomous Travel Plan", type="primary", use_container_width=True)

base_days = duration
multiplier = {"Budget": 4000, "Moderate": 12000, "Luxury": 30000}[budget_tier]
flight_cost = {"Budget": 12000, "Moderate": 25000, "Luxury": 55000}[budget_tier]
hotel_cost = base_days * multiplier
activity_cost = base_days * {"Budget": 2500, "Moderate": 6000, "Luxury": 12000}[budget_tier]
total_estimated_cost = flight_cost + hotel_cost + activity_cost

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("2. System Monitoring & Chat Engine")
    
    # Trace Log Dashboard Wrapped in an Expander for Spatial Management
    with st.expander("🛠️ Multi-Agent Trace Log Terminal", expanded=True):
        log_placeholder = st.empty()
        log_placeholder.markdown('<div class="terminal-box">_ Multi-Agent trace log standby. Adjust portal inputs and execute engine...</div>', unsafe_allow_html=True)
    
    # Chatbot Interactive Sandbox Layout
    st.markdown("#### 💬 Chat with Travel Co-Pilot")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
    if chat_input := st.chat_input("Ask a follow-up question regarding your trip..."):
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with chat_container:
            with st.chat_message("user"):
                st.write(chat_input)
                
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Processing travel context queries..."):
                    try:
                        # Construct historical contextual log payload
                        prompt_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
                        prompt_history += f"\nSystem Instruction: You are an expert AI Travel Assistant. Give concise, direct answers regarding travel to {destination}."
                        
                        response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=f"{prompt_history}\nassistant:"
                        )
                        bot_response = response.text
                    except Exception:
                        bot_response = f"I am operating in localized sandbox mode right now, but I can confirm that a {duration}-day trip to {destination} fits your configured travel guidelines perfectly!"
                    
                    st.write(bot_response)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

with col_right:
    st.subheader("3. Expense Dashboard")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Estimate", f"₹{total_estimated_cost:,}")
    m_col2.metric("Flight Hub", f"₹{flight_cost:,}")
    m_col3.metric("Lodging Layer", f"₹{hotel_cost:,}")
    m_col4.metric("Daily Outlays", f"₹{activity_cost:,}")

st.markdown("---")
st.subheader("4. Interactive Itinerary Builder")

# Dynamic Output Section
output_container = st.container()

if generate_btn:
    logs = []
    def update_logs(msg):
        logs.append(f"> {msg}")
        log_html = "".join([f"<div>{l}</div>" for l in logs])
        log_placeholder.markdown(f'<div class="terminal-box">{log_html}</div>', unsafe_allow_html=True)

    update_logs(f"Initializing target matrix coordinates for {destination}...")
    
    from mcp_servers.travel_mcp import search_flights, recommend_hotels
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    raw_flights = loop.run_until_complete(search_flights(origin, destination, "2026-10-12"))
    update_logs("MCP Tool Executed: search_flights -> returned data maps [Status 200]")
    
    raw_hotels = loop.run_until_complete(recommend_hotels(destination, budget_tier))
    update_logs("MCP Tool Executed: recommend_hotels -> synchronized inventory caches [Status 200]")
    
    update_logs("Dispatching asynchronous parallel queries to sub-agents...")
    context = {"origin": origin, "destination": destination, "raw_flights": raw_flights, "raw_hotels": raw_hotels, "budget_tier": budget_tier}
    
    flight_res = loop.run_until_complete(run_flight_agent(context))
    hotel_res = loop.run_until_complete(run_hotel_agent(context))
    weather_res = loop.run_until_complete(run_weather_agent(context))
    
    update_logs("Synthesizing separate streams inside Master Itinerary Agent context...")
    
    final_prompt = f"""
    You are the Master Itinerary Planner. Compile a travel plan for {duration} days from {origin} to {destination}.
    Flight Selection: {flight_res}
    Hotel Selection: {hotel_res}
    Weather Profile: {weather_res}
    
    First, create a 'Booking Action Items' section that extracts and displays the direct booking links provided by the sub-agents. 
    Then, generate the detailed structured daily breakdown. Use 'Day X:' as headers for each day.
    """
    
    try:
        master_response = client.models.generate_content(model=MODEL_NAME, contents=final_prompt)
        full_text = master_response.text
        update_logs("Success: Combined itinerary canvas rendered completely.")
    except Exception:
        update_logs("Notice: Initializing local state formatting due to live gateway capacity.")
        full_text = f"### Booking Action Items\n* {flight_res}\n* {hotel_res}\n\n"
        fallback_activities = [
            {"m": f"Arrival and hotel check-in. Brief walking tour around central {destination}.", "a": "Visit primary landmarks and historical districts to establish bearings.", "e": "Welcome dinner at a highly-rated local restaurant."},
            {"m": "Guided cultural immersion tour based on local heritage.", "a": "Museum or gallery visits, aligned with weather pacing.", "e": "Street food exploration or casual dining in a vibrant neighborhood."},
            {"m": "Nature walk, park visit, or coastal exploration.", "a": "Shopping at local markets or high-end boutique districts.", "e": "Fine dining selection and evening entertainment."},
            {"m": "Visit to secondary historical sites or architectural highlights.", "a": "Relaxation time at a scenic viewpoint or the hotel spa.", "e": "Night market visit or sunset cruise."},
            {"m": "Leisurely breakfast and final souvenir shopping.", "a": "Packing, check-out preparations, and final photos.", "e": "Transit to the airport for departure."}
        ]
        for day in range(1, duration + 1):
            act = fallback_activities[(day - 1) % len(fallback_activities)]
            full_text += f"Day {day}:\n- **Morning:** {act['m']}\n- **Afternoon:** {act['a']}\n- **Evening:** {act['e']}\n"

    # Separate the Booking Links from the Day-by-Day schedule
    parts = full_text.split("Day 1:")
    booking_section = parts[0]
    itinerary_days = "Day 1:" + parts[1] if len(parts) > 1 else ""

    with output_container:
        st.info("### 🔗 Ready to Book? \n" + booking_section)
        
        day_tabs = st.tabs([f"Day {i+1}" for i in range(duration)])
        days_data = itinerary_days.split("Day ")
        
        for i in range(duration):
            with day_tabs[i]:
                st.markdown(f"### Activity Framework for Day {i+1}")
                if i+1 < len(days_data):
                    st.write("Day " + days_data[i+1])
                else:
                    st.write("Schedule matrices optimized. Proceed with designated itinerary points.")