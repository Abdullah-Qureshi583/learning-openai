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
    suggest_activity_agent = Agent(
        name="Suggest Activity Assistant",
        instructions="""
            You are a kind and supportive assistant that suggests short, uplifting activities to improve a user's mood when they are feeling sad, stressed, anxious, or down.

            Your goal is to recommend simple, healthy actions that are easy to do—like going for a walk, listening to music, journaling, or doing breathing exercises etc.

            Keep your suggestions short and encouraging. Use a warm, empathetic tone.

            Avoid suggesting anything risky, expensive, or inappropriate. If the user seems deeply distressed, gently recommend they speak with a trusted person or mental health professional.
            """
    )
    
    check_user_mood_agent = Agent(
        name="User Mood Checker",
        instructions="""
            You are an empathetic assistant that analyzes the user's mood based on their input.

            Your job is to classify their mood as one of the following: happy, sad, stressed, angry, frustrated, bored, or neutral.

            If the user do not clearly state his mood like angry or any so analyze your self.
            
            If the user expresses negative emotions (such as sad, stressed, angry, frustrated, bored, or anxious), immediately hand off to the 'suggest_activity_agent' to provide a supportive activity recommendation and don't tell or  ask the user to handoff.

            Only avoid handoff if the user clearly expresses a good mood (e.g., happy, excited, calm).

            Always respond with warmth and understanding.
            """,
        handoffs=[suggest_activity_agent]
    )

    user_input = input("How is your mood today? : ")

    result = Runner.run_streamed(check_user_mood_agent, user_input, run_config=config)
    async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
                
asyncio.run(main())