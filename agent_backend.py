

import os
import requests
import json
from dotenv import load_dotenv

# --- LANGCHAIN & GEMINI IMPORTS ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ===============================
# 1. SETUP & CONFIGURATION
# ===============================
load_dotenv()

# API Key Check (Critical Step)
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY is missing in .env file.")
    exit()

if not os.getenv("WEATHER_API_KEY"):
    print("⚠️ Warning: WEATHER_API_KEY is missing. Weather tool will fail.")

# ===============================
# 2. DEFINE TOOLS (LOGIC LAYER)
# ===============================

@tool
def web_search(query: str):
    """Finds information on the internet. Use for current events/news."""
    print(f"    ⚙️ [TOOL CALL] Searching for: '{query}'...")  # Debug print
    try:
        return DuckDuckGoSearchRun().invoke(query)
    except Exception as e:
        return f"Search failed: {e}"

@tool
def get_weather_data(city: str):
    """Get current weather for a city."""
    print(f"    ⚙️ [TOOL CALL] Fetching weather for: '{city}'...") # Debug print
    
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key: return "Error: Weather API Key missing."
    try:
        url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        res = requests.get(url).json()
        if "error" in res: return f"Error: {res['error']['info']}"
        return json.dumps(res['current']) 
    except Exception as e:
        return f"Error fetching weather: {e}"

tools = [web_search, get_weather_data]

# ===============================
# 3. AGENT SETUP (GEMINI)
# ===============================

print("🔌 Connecting to Google Gemini 1.5 Flash...")

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

# Create the Agent Executor
agent_executor = create_react_agent(
    model=llm,    # ✅ Humne wo configure kiya hua object pass kiya
    tools=tools
)
print("✅ Agent is Ready! (Ctrl+C to exit)")

# ===============================
# 4. RUN LOOP (CLI INTERFACE)
# ===============================

def run_chat_loop():
    # Chat History (Session State for Backend)
    chat_history = []

    while True:
        try:
            print("\n" + "="*50)
            user_input = input("🔵 YOU: ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Bye!")
                break
            
            # Add user message to history
            chat_history.append(HumanMessage(content=user_input))

            print("🤖 GEMINI IS THINKING...")
            
            # Run the Agent
            # We use 'invoke' to get the final result, 
            # but the tools inside will print their status automatically.
            response = agent_executor.invoke(
                {"messages": chat_history},
                config={"recursion_limit": 10}
            )

            # Get the final answer text
            final_answer = response["messages"][-1].content
            
            # Update history
            chat_history.append(AIMessage(content=final_answer))

            print(f"🟢 AGENT: {final_answer}")

        except Exception as e:
            print(f"❌ SYSTEM ERROR: {str(e)}")

if __name__ == "__main__":
    run_chat_loop()

