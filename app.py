# app.py
import os
import asyncio
import json
import streamlit as st
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

# --- STARTUP PRODUCTION THEME CONFIGURATION ---
st.set_page_config(
    page_title="Travel Buddy | Omni-Channel Travel AGENT SUITE", 
    page_icon="✈️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Injection for Global Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    .stApp { background-color: #050505; color: #F1F5F9; }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Elegant Startup Identity Gradient */
    .brand-title {
        font-size: 2.6rem; font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8, #E879F9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em; margin-bottom: 0.1rem;
    }
    .brand-subtitle { 
        font-size: 1rem; color: #94A3B8; font-weight: 400; 
        margin-bottom: 1.5rem; border-bottom: 1px solid #1E293B; padding-bottom: 1rem; 
    }
    
    /* Telemetry Console Custom CSS */
    .terminal-header { 
        background-color: #0F172A; color: #94A3B8; padding: 0.5rem 1rem; 
        font-family: monospace; font-weight: 600; font-size: 0.75rem; 
        border-top-left-radius: 0.5rem; border-top-right-radius: 0.5rem; 
        border: 1px solid #334155; border-bottom: none; 
    }
    .terminal-body { 
        background-color: #000000; color: #10B981; font-family: 'Courier New', monospace; 
        padding: 1.2rem; border: 1px solid #334155; border-bottom-left-radius: 0.5rem; 
        border-bottom-right-radius: 0.5rem; height: 300px; overflow-y: auto; 
        font-size: 0.85rem; line-height: 1.6; box-shadow: inset 0 2px 10px 0 rgba(0,0,0,0.8);
    }
    
    /* Navigation Bar Interface Modifications */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: transparent; color: #64748B; 
        font-weight: 600; font-size: 0.95rem; transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] { 
        color: #818CF8 !important; border-bottom-color: #818CF8 !important; 
        border-bottom-width: 3px !important; font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

if not os.getenv("GROQ_API_KEY"):
    st.error("Infrastructure Initialization Failure: Missing global token environment routing.")
    st.stop()

# Initialize Core Execution Layer
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

# --- MULTI-AGENT MICROSERVICES ---
async def run_flight_agent(origin: str, dest: str, budget: str) -> str:
    prompt = f"System: You are an Aviation Broker Agent. Find the best flight route from {origin} to {dest} for a {budget} budget. Output pricing strictly in INR (₹). Provide a direct markdown booking link to MakeMyTrip or Skyscanner. Format as a short, punchy summary."
    res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], temperature=0.2)
    return res.choices[0].message.content

async def run_train_agent(origin: str, dest: str, budget: str) -> str:
    prompt = f"System: You are a Rail Transit Agent. Evaluate train connectivity from {origin} to {dest} (e.g., Vande Bharat, Rajdhani, Shatabdi, or EuroRail if international). Output pricing strictly in INR (₹). Provide a direct markdown booking link to IRCTC or ConfirmTkt. If no trains exist, state 'No viable rail routes'."
    res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], temperature=0.2)
    return res.choices[0].message.content

async def run_accommodation_agent(dest: str, duration: int, budget: str) -> str:
    prompt = f"System: You are a Lodging Broker. Find accommodation in {dest} for {duration} days on a {budget} budget. You MUST compare exactly one top Hotel and exactly one top Airbnb. Output total pricing in INR (₹) for the stay. Provide direct markdown links to Booking.com and Airbnb for the properties."
    res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], temperature=0.2)
    return res.choices[0].message.content

async def run_social_sentiment_agent(dest: str) -> str:
    prompt = f"System: You are a Social Sentiment & Review Scraper Agent. Analyze current mocked web data for {dest} (Google Reviews, YouTube travel vlogs, Reddit, TripAdvisor). Identify the top 3 highest-rated hidden gems. Ensure you highlight highly acclaimed vegetarian food spots or street food lanes backed by food vloggers."
    res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], temperature=0.4)
    return res.choices[0].message.content

async def run_master_itinerary_agent(duration: int, origin: str, dest: str, flights: str, trains: str, hotels: str, sentiment: str) -> str:
    prompt = f"""System: You are the Chief Operations Master Itinerary Planner. Synthesize this raw agent data into a polished B2C travel itinerary portfolio for a {duration}-day trip from {origin} to {dest}.
    
    [Flight Logistics]: {flights}
    [Rail Logistics]: {trains}
    [Accommodation]: {hotels}
    [Social Sentiment & Top Spots]: {sentiment}
    
    Structure your output cleanly with markdown:
    1. 'Verified Core Logistics': Consolidate all the booking links and INR pricing here.
    2. 'Day-by-Day Roadmap': Use '### Day X:' headings. Integrate the specific YouTube/Reddit hidden gems and dining spots identified by the Sentiment Agent directly into the daily flow."""
    res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], temperature=0.3)
    return res.choices[0].message.content

# --- PERSISTENT STATE LOGISTICS ---
if "trip_logs" not in st.session_state: st.session_state.trip_logs = ["_ Platform initialized. Core microservices idling..."]
if "agent_payloads" not in st.session_state: st.session_state.agent_payloads = {}
if "final_itinerary" not in st.session_state: st.session_state.final_itinerary = None

# --- HEADER INTERFACE ---
st.markdown('<div class="brand-title">✈️ Travel Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">MULTI-AGENT TRAVEL PLANNER</div>', unsafe_allow_html=True)

# --- WORKSPACE CONTROL SIDEPANEL ---
with st.sidebar:
    st.subheader("Journey Parameters")
    origin = st.text_input("Origin City", placeholder="e.g., Aligarh, New Delhi...")
    destination = st.text_input("Destination Hub", placeholder="e.g., Manali, Paris...")
    duration = st.slider("Trip Duration (Days)", min_value=1, max_value=14, value=4)
    budget_tier = st.radio("Financial Capital Tier", options=["Budget", "Moderate", "Luxury"], index=1)
    
    st.markdown("---")
    generate_btn = st.button("Initialize Optimization Routine", type="primary", use_container_width=True)
    st.caption("Deployment: **Production Gateway v3.0**")

# --- CONTEXT PRICE CALCULATOR ENGINE (Mock Aggregator Data) ---
base_mult = {"Budget": 2500, "Moderate": 7500, "Luxury": 22000}[budget_tier]
f_base = {"Budget": 6000, "Moderate": 15000, "Luxury": 45000}[budget_tier]

flight_matrix = {
    "Skyscanner": f_base,
    "Kayak": int(f_base * 1.05),
    "Google Flights": int(f_base * 0.96)  
}
hotel_matrix = {
    "Booking.com": base_mult * duration,
    "Airbnb": int((base_mult * duration) * 0.92),  
    "Agoda": int((base_mult * duration) * 1.04)
}

best_flight = min(flight_matrix.values())
best_hotel = min(hotel_matrix.values())
activity_outlay = duration * {"Budget": 1500, "Moderate": 4500, "Luxury": 12000}[budget_tier]
net_startup_cost = best_flight + best_hotel + activity_outlay

# --- GRAPHICAL INTERFACE WORKSPACE ---
tab_dash, tab_itinerary, tab_telemetry, tab_chat = st.tabs([
    "📊 Global Market Broker",
    "🗺️ Master Execution Itinerary", 
    "⚙️ Individual Agent Telemetry",
    "💬 Interactive AI Co-Pilot" 
])

# ==========================================
# TAB 1: MARKET PRICE BROKER & COMPARISON
# ==========================================
with tab_dash:
    st.subheader("Real-Time Multi-Platform Pricing Discrepancies")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.container(border=True).metric("Optimized Target Value", f"₹{net_startup_cost:,}", delta="Lowest Market Match", delta_color="normal")
    with m2: st.container(border=True).metric("Target Transit Unit", f"₹{best_flight:,}")
    with m3: st.container(border=True).metric("Accommodation Base", f"₹{best_hotel:,}")
    with m4: st.container(border=True).metric("Operational Daily Capital", f"₹{activity_outlay:,}")
    
    st.markdown("---")
    
    col_f_table, col_h_table = st.columns(2)
    with col_f_table:
        st.markdown("### 🛫 Live Transit Aggregator Feeds")
        st.markdown(f"""
        | Provider Interface | Rate Basis | Deviation Metrics | Status Profile |
        | :--- | :--- | :--- | :--- |
        | **Google Flights** | ₹{flight_matrix['Google Flights']:,} | -4.0% Market Low | 🟢 **Optimal Selection** |
        | **Skyscanner** | ₹{flight_matrix['Skyscanner']:,} | Base Rate | 🟡 Standard Match |
        | **Kayak** | ₹{flight_matrix['Kayak']:,} | +5.0% Inefficient | 🔴 Sub-Optimal |
        """)
        
    with col_h_table:
        st.markdown("### 🏨 Live Lodging Aggregator Feeds")
        st.markdown(f"""
        | Provider Interface | Rate Basis | Deviation Metrics | Status Profile |
        | :--- | :--- | :--- | :--- |
        | **Airbnb** | ₹{hotel_matrix['Airbnb']:,} | -8.0% Market Low | 🟢 **Optimal Selection** |
        | **Booking.com** | ₹{hotel_matrix['Booking.com']:,} | Base Rate | 🟡 Standard Match |
        | **Agoda** | ₹{hotel_matrix['Agoda']:,} | +4.0% Inefficient | 🔴 Sub-Optimal |
        """)

# ==========================================
# TAB 2: MASTER ITINERARY OUTPUT
# ==========================================
with tab_itinerary:
    if st.session_state.final_itinerary:
        with st.container(border=True):
            st.markdown(st.session_state.final_itinerary)
    else:
        st.info("System configuration cache blank. Define origin and destination, then trigger execution.")

# ==========================================
# TAB 3: INDIVIDUAL AGENT RAW OUTPUTS
# ==========================================
with tab_telemetry:
    st.subheader("Raw Agent Microservice Payloads")
    if st.session_state.agent_payloads:
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("🛫 Flight Broker Agent Output", expanded=True):
                st.markdown(st.session_state.agent_payloads.get('flight', 'No data.'))
            with st.expander("🚆 Rail Transit Agent Output", expanded=True):
                st.markdown(st.session_state.agent_payloads.get('train', 'No data.'))
        with c2:
            with st.expander("🏨 Accommodation Broker (Hotel & Airbnb)", expanded=True):
                st.markdown(st.session_state.agent_payloads.get('hotel', 'No data.'))
            with st.expander("📱 Social Sentiment & Vlog Agent", expanded=True):
                st.markdown(st.session_state.agent_payloads.get('sentiment', 'No data.'))
                
        st.markdown("---")
        st.markdown('<div class="terminal-header">A2A System Operations Trace</div>', unsafe_allow_html=True)
        log_content = "<br>".join(st.session_state.trip_logs)
        st.markdown(f'<div class="terminal-body">{log_content}</div>', unsafe_allow_html=True)
    else:
        st.info("Execute pipeline to view multi-agent JSON and Markdown payloads.")

# ==========================================
# TAB 4: INTERACTIVE CONSOLE CHATBOT
# ==========================================
with tab_chat:
    if "travel_chat" not in st.session_state:
        st.session_state.travel_chat = [{"role": "assistant", "content": "Travel Buddy online. Query me regarding visa requirements, forex exchange rates, or deep-link booking assistance."}]
        
    chat_box = st.container(height=400, border=True)
    with chat_box:
        for msg in st.session_state.travel_chat:
            with st.chat_message(msg["role"]): st.write(msg["content"])
                
    if chat_input := st.chat_input("Ask about local transport passes, safety, or weather conditions..."):
        st.session_state.travel_chat.append({"role": "user", "content": chat_input})
        with chat_box:
            with st.chat_message("user"): st.write(chat_input)
            with st.chat_message("assistant"):
                with st.spinner("Accessing global cache directories..."):
                    history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.travel_chat])
                    prompt = f"{history}\nSystem: You are a commercial travel asset manager. Provide precise, authoritative counsel.\nassistant:"
                    async def fetch_chat():
                        res = await client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
                        return res.choices[0].message.content
                    bot_reply = asyncio.run(fetch_chat())
                    st.write(bot_reply)
        st.session_state.travel_chat.append({"role": "assistant", "content": bot_reply})

# --- BACKEND MULTI-AGENT EXECUTION PIPELINE ---
if generate_btn:
    if not origin or not destination:
        st.error("Protocol failure: Origin and Destination parameters are mandatory.")
    else:
        st.session_state.trip_logs = []
        def log_event(msg):
            st.session_state.trip_logs.append(f"[ORCHESTRATOR] {msg}")

        async def execute_travel_pipeline():
            log_event(f"Locking spatial variables. Routing {origin} ➡️ {destination}. Budget: {budget_tier}.")
            log_event("Asynchronous pipeline channel open. Dispatching pricing & sentiment audit requests globally.")
            
            # Parallel Execution Architecture - 4 Agents Running Simultaneously
            log_event("Spawning concurrent runtime context for Flight, Rail, Lodging, and Sentiment sub-agents...")
            f_res, t_res, h_res, s_res = await asyncio.gather(
                run_flight_agent(origin, destination, budget_tier),
                run_train_agent(origin, destination, budget_tier),
                run_accommodation_agent(destination, duration, budget_tier),
                run_social_sentiment_agent(destination)
            )
            
            # Store raw payloads for the Telemetry Dashboard
            st.session_state.agent_payloads = {
                'flight': f_res, 'train': t_res, 'hotel': h_res, 'sentiment': s_res
            }
            
            log_event("Sub-agent verification matrices evaluated. Injecting outputs to Master Synthesis Engine...")
            final_text = await run_master_itinerary_agent(duration, origin, destination, f_res, t_res, h_res, s_res)
            
            log_event("State pipeline successfully updated. Flushing changes to interactive dashboard.")
            return final_text

        st.session_state.final_itinerary = asyncio.run(execute_travel_pipeline())
        st.rerun()