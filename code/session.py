from agents import Agent, Runner, OpenAIChatCompletionsModel,SQLiteSession, trace
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
    
    # session = SQLiteSession("conversation_123")

    
    
    # while True:
    #     user_input = str(input("How can I help you? "))
    #     if user_input != "exit":
    #         result = await Runner.run(
    #             starting_agent=agent, 
    #             input=user_input, 
    #             run_config=config, 
    #             session=session
    #         )
    #     else:
    #         exit()

    #     print("🟢 First result:", result.final_output)
        
        
        
    
    # user_input2 = str(input("what do you ask about? :"))
    # result = await Runner.run(
    #     agent,
    #     input=user_input2,
    #     run_config=config, 
    #     session=session
    # )
    # print("Second Result : " ,result.final_output) 




    thread_id = "thread_123"  # Example thread ID
    with trace(workflow_name="Conversation", group_id=thread_id):
        # First turn
        result = await Runner.run(agent, "What city is the Golden Gate Bridge in?", run_config=config)
        print(result.final_output)
        # San Francisco

        # Second turn
        new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
        result = await Runner.run(agent, new_input, run_config=config)
        print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())
    