import asyncio # Asynchronous programming support
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig  # Used to configure how the agent run behaves
from openai import AsyncOpenAI    # Asynchronous OpenAI-compatible client for making API calls
import os
from dotenv import load_dotenv    # For loading environment variables from a .env file

# Load API keys and environment variables from the .env file
load_dotenv()

# Get Gemini API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set the Gemini model and base URL for OpenAI-compatible API
MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Initialize the OpenAI-compatible client with Gemini settings
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

# Create a chat completion model using Gemini through the OpenAI-compatible client
model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

# -------------------- Tool Definitions --------------------

# Define a simple greeting tool that can be called by the agent
@function_tool
def greet(name: str) -> str:
    return f"Hello, {name}! How can I assist you today?"

# Define a simple farewell tool that can be called by the agent
@function_tool
def farewell(name: str) -> str:
    return f"Goodbye, {name}! Have a great day!"

# -------------------- Run Configuration --------------------

# Configure how the agent runs (which model to use, disable tracing, etc.)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True  # Disable tracing for simplicity (can be set to False for debugging)
)

# -------------------- Main Async Function --------------------

# This is the main function that controls agent behavior
async def main():
    # Create a greeting agent with instructions on how to greet users
    greeting_agent = Agent(
        name="Greeting Agent",
        instructions="You are a greeting agent. Your task is to greet the user in a friendly manner.",
        model=model,
    )

    # Create a farewell agent with instructions on how to say goodbye
    farewell_agent = Agent(
        name="Farewell Agent",
        instructions="You are a farewell agent. Your task is to say goodbye to the user in a friendly manner.",
        model=model,
    )

    # Create a triage agent that decides whether to handle input or hand it off
    agent = Agent(
        name="Triage Agent",
        instructions=(
            "You are a triage agent. Your task is to read the user prompt and "
            "if this is relevant to the greeting or farewell agents, assess the user's needs and "
            "route them to the appropriate agent. Otherwise, try to answer the question yourself."
        ),
        handoffs=[greeting_agent, farewell_agent],  # Allow delegation to greeting or farewell agents
    )

    # Prompt user for input
    user_input = str(input("Ask to ai: "))

    # Run the main agent and pass in the user input along with the run config
    result = await Runner.run(agent, user_input, run_config=config)

    # Print the final result from the agent
    print(result)

# Entry point for the script
if __name__ == "__main__":
    asyncio.run(main())
