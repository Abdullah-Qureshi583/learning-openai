from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent

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
    )

    user_input = str(input("How can I help you? "))
    result = await Runner.run(agent,  input=user_input, run_config=config)
    print("The responce from the agent is : ", result.final_output)
    

if __name__ == "__main__":
    asyncio.run(main())