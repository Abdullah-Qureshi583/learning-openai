# ------------------ Imports ------------------
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool  # Import tools to create agents and run them
from openai import AsyncOpenAI  # For connecting to OpenAI-compatible models
from dotenv import load_dotenv  # To load API keys securely from .env file
import os  # To access environment variables

# ------------------ Load Environment Variables ------------------
load_dotenv()  # Load variables from the .env file

# Get the Gemini API key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Define the model name and API endpoint for Gemini
MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# ------------------ Setup Gemini Client ------------------
# Create a client that is compatible with OpenAI API structure, but actually talks to Gemini
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

# Connect the client to the model via a chat completion interface
model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

# ------------------ Tools for Agent ------------------
# Create a function tool that the agent can call when it wants to greet someone
@function_tool
def greet(name: str) -> str:
    return f"Hello, {name}! How can I assist you today?"

# Another tool for saying goodbye
@function_tool
def farewell(name: str) -> str:
    return f"Goodbye, {name}! Have a great day!"

# ------------------ Create Agent ------------------
# This agent is responsible for greetings
greeting_agent = Agent(
    name="Greeting Agent",
    instructions="You are a greeting agent. Your task is to greet the user in a friendly manner.",
    model=model,  # Use the Gemini model we configured
)

# ------------------ Run Agent ------------------
# Ask the user to input something from the terminal
user_input = str(input("Ask to ai: "))

# Run the agent synchronously with the user input and store the response
runner = Runner.run_sync(greeting_agent, user_input)

# Print the full response from the agent
print(runner)
