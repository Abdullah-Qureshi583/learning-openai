from agents import enable_verbose_stdout_logging
import asyncio 
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI   
import os
from agents.run import RunConfig
from dotenv import load_dotenv   

enable_verbose_stdout_logging()
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


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


async def main():

    greeting_agent = Agent(
        name="Greeting Agent",
        instructions="You are a greeting agent. Your task is to greet the user in a friendly manner.",
        model=model,
    )
    farewell_agent = Agent(
        name="Farewell Agent",
        instructions="You are a farewell agent. Your task is to say goodbye to the user in a friendly manner.",
        model=model,
    )

    
    triage_agent = Agent(
        name="Triage Agent",
        instructions=(
            "You are a triage agent. Your task is to read the user prompt and "
            "if this is relevant to the greeting or farewell agents, assess the user's needs and "
            "route them to the appropriate agent. Otherwise, try to answer the question yourself."
        ),
        handoffs=[greeting_agent, farewell_agent]
    )

    # Prompt user for input
    user_input = str(input("Ask to ai: "))

    
    result =await Runner.run(triage_agent, user_input, run_config=config)

    print(result)

# Entry point for the script
if __name__ == "__main__":
    asyncio.run(main())
