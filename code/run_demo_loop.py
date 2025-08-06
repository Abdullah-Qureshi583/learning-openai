# this use to talk with the llm continuosly without any looping
from agents import Agent, OpenAIChatCompletionsModel, run_demo_loop
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import os
from agents.run import RunConfig

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

async def main():
    agent = Agent(
        name="Helpful Assistant",
        instructions="You are a helpful assistant.",
        model=model
    )

    await run_demo_loop(agent)



if __name__ == "__main__":
    asyncio.run(main())