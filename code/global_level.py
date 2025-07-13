# Import necessary modules and functions from the agents framework
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
import os
from dotenv import load_dotenv  # To load environment variables from .env file

# ------------------- Load Environment Variables -------------------
load_dotenv()

# Get Gemini API key from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set the Gemini model name and compatible base URL for OpenAI-style API
MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# ------------------- Set Up OpenAI-Compatible Gemini Client -------------------
# This creates an OpenAI-style client that connects to Gemini using OpenRouter-like compatibility
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

# ------------------- Agent Framework Configuration -------------------
set_tracing_disabled(True)  # Turn off tracing (used for debugging or logging, not needed here)
set_default_openai_api("chat_completions")  # Set the type of OpenAI API being used (chat-style)
set_default_openai_client(external_client)  # Set the Gemini client as the default OpenAI client

# ------------------- Create and Run the Agent -------------------
# Define an agent with a name, instructions, and the model
agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",  # This tells the agent how to behave
    model="gemini-2.5-flash"
)

# Run the agent synchronously on the user prompt
result = Runner.run_sync(agent, "Hello")  # User input is "Hello"

# Print only the final output from the agent
print(result.final_output)
