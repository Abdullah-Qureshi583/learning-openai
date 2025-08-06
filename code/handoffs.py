# handoffs use deligate the task to another agent
# handoff is used to define and override the specific agent like its name , dexcription etc
# if the name is changes using handoff so the llm will see the new name even use the agent with that name even the detailis not related

from agents import Agent, Runner, OpenAIChatCompletionsModel,handoff, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import os
from agents.run import RunConfig

load_dotenv()
enable_verbose_stdout_logging()

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
   
    python_agent = Agent(
        name="Python Assistant",
        instructions="You are a python assistant, that tells just about the python queries ask by the user. give the short answer.",
        handoff_description="This python assistant tell every thing related to python."
    )
    
    historical_agent = Agent(
        name="Historical Assistant",
        instructions="You are a Historical assistant, that tell just about the historical places ask by the user. give the short answer.",
        handoff_description="This agent just tells about the historical places"
    )
    
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You are a triage agent, your task is to handoff the task to the relevant agent. If the agent for that task is not available return the user",
        handoffs=[ historical_agent,
                   handoff(
                    python_agent,
                    tool_name_override="weather_assistant",
                    tool_description_override="Handles weather questions."
                   )
                ]    
    )

    user_input = str(input("How can I help you? "))
    result = await Runner.run(triage_agent, input=user_input, run_config=config)

    print("🟢Response:", result)

if __name__ == "__main__":
    asyncio.run(main())