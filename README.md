# Autonomous Multi-Agent Travel Engine ✈️

An advanced, production-grade multi-agent AI travel orchestration platform. This system leverages the **Google Gemini 2.5 Flash architecture** coupled with native **Model Context Protocol (MCP)** infrastructure layers to seamlessly coordinate parallel sub-agents (Flight, Hotel, Weather) into a consolidated, dynamic travel layout.

---

## 🚀 Core Architecture Modules

The engine features a fully responsive, data-driven web dashboard divided into four synchronized modular layers:

1. **Travel Planning Portal:** A flexible parameter control configuration panel located in the sidebar, managing real-time coordinates, timeline bounds, and structural budget profiles.
2. **Travel Chat Assistant & Tracing Terminal:** A live, low-latency agent-to-agent (A2A) trace log window that streams internal cognitive process states, MCP server calls, and tool parameters in real time.
3. **Expense Dashboard:** A centralized financial accounting view that auto-calculates total travel outlays across airline hubs, accommodation layers, and active daily expenditures—completely localized in **Indian Rupees (INR, ₹)**.
4. **Interactive Itinerary Builder:** A dynamic, multi-day tabbed system mapping curated travel timelines complete with direct booking action integrations to verified provider web properties.

---

## 🛠️ Tech Stack & Infrastructure

* **Orchestration Framework:** Python 3.11+, Asyncio (Asynchronous Parallel Tasking)
* **Intelligence Layer:** Google GenAI SDK (`gemini-2.5-flash`)
* **Tool Layer:** Model Context Protocol (MCP) Standard Server Protocol
* **User Interface Layout:** Streamlit Web Application Framework
* **Environment Security:** Python-Dotenv Layer (Protected API Key Storage)

---

## 📦 Project Directory Structure

```text
travel-planner-agents/
├── mcp_servers/
│   └── travel_mcp.py        # Core MCP infrastructure & vendor databases
├── app.py                   # Streamlit Orchestrator & Web Layout Engine
├── orchestrator.py          # Legacy/Alternative execution module
├── .gitignore               # Strict tracking exclusion filter (.env, caches)
├── requirements.txt         # Project dependencies map
└── README.md                # System documentation
⚙️ Installation & Setup Deployment
Follow these sequential setup instructions to get the autonomous multi-agent engine running locally on your workstation.

1. Clone the Workspace
Bash
git clone [https://github.com/prabalvarshney21/travel-planner-agents.git](https://github.com/prabalvarshney21/travel-planner-agents.git)
cd travel-planner-agents
2. Configure Local Virtual Environment
Bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
3. Install System Dependencies
Bash
pip install -r requirements.txt
4. Inject Environment Variables
Create a file named .env in the root folder and provide your unique API credentials:

Plaintext
GEMINI_API_KEY=your_actual_gemini_api_key_here
(Note: The configuration is fully secured; the .env file is natively blocked by the repository's .gitignore rules to prevent credential leaks).

🖥️ Running the Application
Execute the engine orchestrator via your local stream console:

Bash
python -m streamlit run app.py
The browser view will spin up automatically on your local port address: http://localhost:8501.

🔒 Security & Compliance Safeguards
Credential Isolation: Strict API environment isolation rules enforced across deployment profiles.

Resilient Graceful Fallbacks: Equipped with an intelligent localized mock-matrix simulation layer to retain structural layout integrity even during live external gateway latency or 503 server load spikes.


### Step 3: How to Push it to GitHub
Once the file is saved in VS Code, open your integrated terminal (`Ctrl + \``) and run these three commands to send this new file up to your repository:

```powershell
git add README.md
git commit -m "Docs: Restore and finalize project README"
git push origin main