from agents import Agent, Runner, function_tool  # Core agent framework components
from agents.extensions.models.litellm_model import LitellmModel  # LiteLLM wrapper for external model usage
import os  # For accessing environment variables

# ------------------- Model Configuration -------------------

MODEL = 'gemini/gemini-2.0-flash'  # Google Gemini model ID via LiteLLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Load Gemini API key from environment variable

# ------------------- Tool Definition -------------------

# Define a custom tool that can be called by the agent
@function_tool
def get_weather(city: str) -> str:
    print(f"[debug] getting weather for {city}")  # Debug message for developer
    return f"The weather in {city} is sunny."  # Simulated weather response

# ------------------- Agent Setup -------------------

# Create an agent with specific behavior instructions
agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus.",  # Unique instruction to reply only using haiku style
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),  # Use Gemini model via LiteLLM
)

# ------------------- Agent Execution -------------------

# Synchronously run the agent on a user query
result = Runner.run_sync(agent, "What's the weather in Tokyo?")

# Print only the final output (the haiku)
print(result.final_output)
