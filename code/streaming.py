# have docs
# https://github.com/Abdullah-Qureshi583/learning-openai/blob/main/docs/streaming_guide.md
from openai import AsyncOpenAI
import asyncio
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel,ItemHelpers, function_tool
from dotenv import load_dotenv
import random
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

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)

async def main():
    
    # raw response streaming:
    
    # agent = Agent(name="AI Assistant", instructions="You are a helpful AI assistant",model=model)
    # user_input = str(input("How can i help you today? : "))
    # result = Runner.run_streamed(agent,user_input)
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):            
    #         print(event.data.delta, end="", flush=True)
    
    
    # All other response
    joker_agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )
    
    triage_agent = Agent(
        name="Triage Agent",
        instructions="you are a triage agent if the user ask about the joke so handoff to the \"joker_agent\".",
        handoffs=[joker_agent]
    )

    user_input = str(input("How can I help you? "))
    result = Runner.run_streamed(triage_agent,  input=user_input,run_config=config)
    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")
    


if __name__ == "__main__":
    asyncio.run(main())
