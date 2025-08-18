# there are 3 type of tools
# 1. hosted tools
# 2. Function Tool
# 3. Function as tool


from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool, enable_verbose_stdout_logging,run_demo_loop

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import os
from agents.run import RunConfig

# enable_verbose_stdout_logging()
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

# function tool
async def main():   
    
    @function_tool(name_override="get_languages",description_override="get the languages for the specific city")
    async def fetch_weather(city:str)-> str:
        return f"The languages usually spoken in {city} are urdu and panjabi."
        # return f"The weather in {city} is cloudy."
   
    agent = Agent(
        name="Assistant",
        tools=[fetch_weather],  
        model=model
    )

            
    # user_input = str(input("How can I help you? "))
    # result = await Runner.run(agent, input=user_input, run_config=config)
    # print("🟢Response:", result.final_output)
    
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())



