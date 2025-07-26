from agents import Agent, Runner, OpenAIChatCompletionsModel
import asyncio
import os 
from dotenv import load_dotenv
from openai import AsyncOpenAI

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
async def main ():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())