

import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv

# --- IMPORTS (Your Working Backend) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ===============================
# 1. PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Research & Weather Assistant",
    page_icon="🧪",
    layout="wide"
)

load_dotenv()

# Verify API Key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Critical Error: GOOGLE_API_KEY is missing.")
    st.stop()

# ===============================
# 2. CUSTOM UI/UX (The Magic Part ✨)
# ===============================
st.markdown("""
<style>
    /* 1. Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* 2. Remove Streamlit Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Floating Animated Background Objects */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(10deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    .floating-shape {
        position: fixed;
        width: 150px;
        height: 150px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20%;
        z-index: 0;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        pointer-events: none; /* Allows clicking through shapes */
    }
    
    .shape-1 { top: 10%; left: 5%; animation: float 6s ease-in-out infinite; }
    .shape-2 { top: 70%; right: 5%; animation: float 8s ease-in-out infinite; width: 100px; height: 100px; border-radius: 50%; }
    .shape-3 { top: 40%; left: 80%; animation: float 7s ease-in-out infinite; width: 80px; height: 80px; }

    /* 4. Title Styling */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
        text-shadow: 0px 0px 30px rgba(0, 198, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.2rem;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }

    /* 5. Chat Message Styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 6. Footer Styling */
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        padding: 10px 0;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 999;
    }
    
    .tech-badge {
        display: inline-block;
        padding: 5px 15px;
        margin: 0 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.2s;
    }
    
    .tech-badge:hover {
        transform: scale(1.1);
        background: rgba(255, 255, 255, 0.2);
        cursor: pointer;
    }

    /* Badge Colors */
    .lc { border-color: #f3c138; } 
    .lg { border-color: #e040fb; } 
    .gm { border-color: #4285F4; } /* Google Blue */
    .st { border-color: #ff4b4b; } 
    
</style>

<div class="floating-shape shape-1"></div>
<div class="floating-shape shape-2"></div>
<div class="floating-shape shape-3"></div>

""", unsafe_allow_html=True)

# ===============================
# 3. BACKEND LOGIC (Gemini)
# ===============================

@tool
def web_search(query: str):
    """Finds information on the internet."""
    try:
        return DuckDuckGoSearchRun().invoke(query)
    except Exception as e:
        return f"Search failed: {e}"

@tool
def get_weather_data(city: str):
    """Get current weather for a city."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key: return "Error: Weather API Key missing."
    try:
        url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        res = requests.get(url).json()
        if "error" in res: return f"Error: {res['error']['info']}"
        return json.dumps(res['current']) 
    except Exception as e:
        return f"Error: {e}"

tools = [web_search, get_weather_data]

# Using 'gemini-flash-latest' (Because it's stable and free)
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
    max_retries=2,
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }
)

agent_executor = create_react_agent(llm, tools)

# ===============================
# 4. FRONTEND UI INTERACTION
# ===============================

# Header Title
st.markdown('<div class="main-title">Research & Weather Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Autonomous AI Agents</div>', unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.content)

# Input Area
user_input = st.chat_input("Ask about weather, research topics, or general knowledge...")

if user_input:
    # 1. Show User Message
    st.chat_message("user", avatar="👤").markdown(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))

    # 2. Agent Processing
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Agent is thinking... 🧠"):
            try:
                response = agent_executor.invoke(
                    {"messages": st.session_state.messages},
                    config={"recursion_limit": 10}
                )
                
                final_ans = response["messages"][-1].content
                st.markdown(final_ans)
                st.session_state.messages.append(AIMessage(content=final_ans))
            
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")

# ===============================
# 5. FOOTER (Tech Stack)
# ===============================
footer_html = """
<div class="footer-container">
    <span class="tech-badge lc">🦜🔗 LangChain</span>
    <span class="tech-badge lg">🕸️ LangGraph</span>
    <span class="tech-badge gm">⚡ Gemini</span>
    <span class="tech-badge st">👑 Streamlit</span>
    <span class="tech-badge">🤖 AI Agents</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
