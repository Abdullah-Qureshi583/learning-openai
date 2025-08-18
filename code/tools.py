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
MODEL = "gemini-2.5-flash"

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
async def function_tool_main():   
    
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


# function as a tool
async def agent_as_tool():   
        
    spanish_agent = Agent(
        name="Spanish agent",
        instructions="You translate the user's message  just to Spanish",
        model=model
        
    )

    french_agent = Agent(
        name="French agent",
        instructions="You translate the user's message  just to French",
        model=model
        
    )
    
    
    orchestrator_agent = Agent(
        name="orchestrator_agent",
        instructions=(
            "You are helpful assistant who reply the user queries."
            # "If the user want to translate  so use the tools given to you to translate."
            # "Don't translate until user ask to translate."
            # "If asked for multiple translations, you call the relevant tools."
            # "If the user ask about to translate and other task that you cannot, so translate and reply for the other tasks."
            # # "If user ask for different languages instead of spanish and french so say don't know in a concise way"
        ),
        # tools=[
        #     spanish_agent.as_tool(
        #         tool_name="translate_to_spanish",
        #         tool_description="Translate the user's message to Spanish",
        #     ),
        #     french_agent.as_tool(
        #         tool_name="translate_to_french",
        #         tool_description="Translate the user's message to French",
        #     ),
        # ],
        model=model
        
        # handoffs=[french_agent,spanish_agent]
    )
                
    while True:
        user_input = str(input("How can I help you? "))
        if user_input.strip().lower() in ["exit", "quit"]:
            return
        result = await Runner.run(orchestrator_agent, input=user_input)
        print("🟢Response:", result)
        

if __name__ == "__main__":
    # asyncio.run(function_tool_main())
    asyncio.run(agent_as_tool())



# function tool



