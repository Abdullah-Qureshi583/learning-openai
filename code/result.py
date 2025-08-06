from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.memory import SQLiteSession
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
    session = SQLiteSession("result_conversation")
    
    python_agent = Agent(
        name="Python Assistant",
        instructions="You are a python assistant, that tells just about the python queries ask by the user. give the short answer."
    )
    
    historical_agent = Agent(
        name="Historical Assistant",
        instructions="You are a Historical assistant, that tell about the historical places and talks about the history ask by the user. give the short answer."          
    )
    
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You are a triage agent, your task is to handoff the task to the relevant agent.",
        handoffs=[ historical_agent,python_agent]    
    )
        
    while True:
        user_input = str(input("How can I help you? "))
        if user_input == "exit":
            exit()
        
        result = await Runner.run(triage_agent, input=user_input, run_config=config, session=session)
        print("🟢Response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
    
    