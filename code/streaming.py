from openai import AsyncOpenAI
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client=client   
)

async def main():
    
    agent = Agent(name="AI Assistant", instructions="You are a helpful AI assistant",model=model)
    user_input = str(input("How can i help you today? : "))
    result = Runner.run_streamed(agent,user_input)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):            
            print(event.data.delta, end="|", flush=True)
    

if __name__ == "__main__":
    asyncio.run(main())



