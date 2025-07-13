import asyncio
from dotenv import load_dotenv  # For loading environment variables
import os
from openai import AsyncOpenAI  # Asynchronous OpenAI-compatible client for making API requests
from agents import Agent, Runner, OpenAIChatCompletionsModel  # Core tools from the `agents` package

# ---------------- Load API Key ------------------

# Load environment variables from .env file
load_dotenv()

# Get the OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Base URL for OpenRouter API
BASE_URL = "https://openrouter.ai/api/v1"

# Choose the model to use
# You tested other models but selected the one below due to performance
MODEL = "openai/gpt-4o-mini"  # Fast and smart model suitable for your task

# ---------------- Client and Model Setup ------------------

# Create the OpenAI-compatible client for OpenRouter
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# Wrap the selected model using OpenAIChatCompletionsModel
model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

# ---------------- Main Function ------------------

# Define the async main function to run the translation agent
async def main():
    # Create an Agent with instructions to translate text into English
    # and convert active voice to passive and passive to active (keeping original too)
    agent = Agent(
        name="Translator Assistant",
        instructions=(
            "You are a helpful assistant who translates the user prompt in English "
            "and turns it into active or passive voice. If the sentence is active, convert it to passive, "
            "and if it’s passive, convert it to active. Also show the original text."
        ),
        model=model,
    )

    # Run the agent with the given user prompt (in Urdu)
    result = await Runner.run(
        agent,  # Agent that should handle the request
        "Mera naam kya ha",  # User's input text
    )

    # Print the final processed response (translation and conversion)
    print(result.final_output)

    # Print full result object for debugging or more insights
    print(result)

# ---------------- Script Entry Point ------------------

# Run the main function using asyncio event loop
asyncio.run(main())
