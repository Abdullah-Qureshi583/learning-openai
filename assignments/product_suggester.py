from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from agents.run import RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = "gemini-2.0-flash"

client = AsyncOpenAI(
    api_key = GEMINI_API_KEY,
    base_url = BASE_URL
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

async def main():    
    agent = Agent(
        name="Smart Store Agent",
        instructions="""
            You are a smart and friendly store assistant.

            When a user describes a need, symptom, or problem, suggest the most appropriate product they could typically find in a pharmacy or general store. Then, briefly explain **why** that product is helpful.

            Be concise, helpful, and use a polite tone.

            If the issue seems serious or beyond general self-care (e.g., chest pain, high fever), politely recommend that the user see a healthcare professional instead of suggesting a product.

            Only suggest safe, over-the-counter items unless asked for something specific.
            
            Do not mention specific brand names unless the user requests it.
        """
    )

    user_input = str(input("What disease do you want to ask about? :"))
    result = Runner.run_streamed(agent, input=user_input, run_config=config)

    async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

asyncio.run(main())