from agents import Agent, Runner, OpenAIChatCompletionsModel,SQLiteSession
# here, i was getting the error as module not found when using SQLiteSession so i update the version of openai 
# from openai.memory import SQLiteSession

# from agents.momory import SQLiteSession
# from agents.memory import SQLiteSession

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
        name="Assistant",
        instructions="Reply very concisely.",
    )
    
    # session = "conversation_123"
    session = SQLiteSession("conversation_123")

    user_input = str(input("How can I help you? "))
    result = await Runner.run(
        starting_agent=agent, 
        # input="What city is the Golden Gate Bridge in?",
        input=user_input, 
        run_config=config, 
        session=session
    )

    print("🟢 First result:", result.final_output)
    
    user_input2 = str(input("what do you adsk about? :"))
    result = await Runner.run(
        agent,
        # "What state is it in?",
        input=user_input2,
        run_config=config, 
        
        session=session
    )
    print("Second Result : " ,result.final_output) 



if __name__ == "__main__":
    asyncio.run(main())