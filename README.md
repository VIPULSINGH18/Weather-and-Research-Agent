<div align="center">

# 🧪 Research & Weather Assistant Agent
### An Autonomous AI Agent powered by LangGraph, LLaMA-3 & Groq

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-green?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-🕸️-blue?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

<br />

<img src="https://via.placeholder.com/800x400.png?text=Agent+Dashboard+Preview" alt="Agent Dashboard" width="800"/>

<br />

**A production-style AI agent that thinks, decides, acts, and stops safely.** *Not just a text generator — an engineered system.*

[View Demo](#) · [Report Bug](issues) · [Request Feature](issues)

</div>

---

## 🚀 Project Overview

This project is an **end-to-end autonomous AI agent system**. Unlike standard chatbots that simply predict the next word, this agent uses the **ReAct (Reason + Act)** paradigm to solve complex queries.

It autonomously determines *if* it needs to search the web, check the weather, or answer directly. It features a robust **confidence scoring system** to let users know how reliable the answer is.

### 🌟 Key Capabilities
| Feature | Description |
| :--- | :--- |
| **🌍 Real-Time Weather** | Fetches live weather data for any global location via Weatherstack API. |
| **📰 Live Research** | Performs web searches for current events (beyond the LLM's training cutoff). |
| **🧠 Autonomous Reasoning** | Uses `LangGraph` to loop through Thought → Action → Observation. |
| **📊 Confidence Scoring** | Self-evaluates its answers and displays a confidence badge (High/Low) in the UI. |
| **🛑 Safety Loops** | Implements recursion limits to prevent infinite agent loops and handle tool failures gracefully. |

---

## 🧠 Architecture & Engineering

This project demonstrates **AI Engineering** concepts over simple prompt engineering.

```mermaid
graph TD
    User(User Query) --> Agent[🤖 ReAct Agent]
    Agent -->|Decides Tool Needed| Router{Router}
    
    Router -->|Need News?| Search[🔎 DuckDuckGo Tool]
    Router -->|Need Weather?| Weather[☁️ Weather API]
    
    Search --> Agent
    Weather --> Agent
    
    Agent -->|Reasoning Loop| Agent
    Agent -->|Confident Answer| Final[✅ Final Answer + Confidence Score]
    Final --> UI[🖥️ Streamlit Frontend]


The ReAct Loop
Thought: The agent analyzes the user request.

Decision: It chooses a tool (Search, Weather) or decides to answer.

Action: It executes the Python function for the tool.

Observation: It reads the tool's output (JSON/Text).

Repeat: It loops until it has enough data to satisfy the user.

🧰 Tech Stack
Brain: Groq (LLaMA-3.3-70B) - Selected for ultra-low latency inference.

Orchestration: LangChain & LangGraph - For stateful agent cycles.

Tools: DuckDuckGo Search & Weatherstack API.

Frontend: Streamlit - With custom CSS for a production-grade dark theme.

Language: Python 3.10+

📂 Project Structure
Bash

Research-Weather-Agent/
│
├── agent_frontend.py    # 🎨 Main Streamlit App + UI Logic
├── agent_backend.py     # 🧠 Core Agent Logic (LangGraph setup)
├── .env                 # 🔐 API Keys (Keep secret!)
├── requirements.txt     # 📦 Python Dependencies
└── README.md            # 📄 Documentation
⚡ Getting Started
1. Clone the Repository
Bash

git clone [https://github.com/yourusername/Research-Weather-Agent.git](https://github.com/yourusername/Research-Weather-Agent.git)
cd Research-Weather-Agent
2. Set Up Virtual Environment
Bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Configure Environment Keys
Create a .env file in the root directory:

Ini, TOML

GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weatherstack_api_key_here
5. Run the Agent 🚀
Bash

streamlit run agent_frontend.py
🎯 Why This Project Matters (Recruiter POV)
This project moves beyond "calling an API" to building a reliable system. Key engineering decisions included:

Control Flow: Using LangGraph instead of simple chains to allow cyclic reasoning (Loops).

Reliability: Implementing recursion_limit to ensure the agent doesn't get stuck in infinite thought loops.

User Trust: The Confidence Score mechanism ensures the user knows when the AI is hallucinating versus when it cites sources.

Error Handling: If a tool (like Weather API) fails, the agent catches the error and informs the user instead of crashing.

🚧 Future Roadmap
[ ] RAG Integration: Connect to local PDFs for document-based Q&A.

[ ] Multi-Agent System: Separate 'Research Agent' and 'Writer Agent'.

[ ] Source Citations: Hyperlink specific URLs used in the final answer.

<div align="center">

👤 Author
Vipul Kumar Singh AI / ML Engineer | Agentic AI Enthusiast

Focused on building reliable, controllable, production-ready AI systems.

LinkedIn • GitHub

</div>
