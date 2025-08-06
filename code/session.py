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
    
    session = SQLiteSession("conversation_123")
    # session = SQLiteSession("conversation_123","./conversation_history.txt")
    

    
    # ===================================================
    # ask with session history until exit
    while True:
        user_input = str(input("How can I help you? "))
        if user_input != "exit":
            result = await Runner.run(
                starting_agent=agent, 
                input=user_input, 
                run_config=config, 
                session=session
            )
        else:
            exit()

        print("🟢 First result:", result.final_output)
        
        
    # =====================================================================
    # done the history manage by manually doing using to_input_list() manually
    
    # thread_id = "thread_123"  # Example thread ID
    # with trace(workflow_name="Conversation", group_id=thread_id):
    #     # First turn
    #     user_input = str(input("Enter your query here?"))
    #     result = await Runner.run(agent, user_input, run_config=config)
    #     print(result.final_output)
    #     # San Francisco

    #     # Second turn
    #     user_input2 = str(input("What do you want to ask about this?"))
    #     new_input = result.to_input_list() + [{"role": "user", "content": user_input2}]
    #     result = await Runner.run(agent, new_input, run_config=config)
    #     print(result.final_output)


    
    # new_items = [
    #     {"role": "user", "content": "My name is Abdullh Qureshi"},    
    #     {"role": "assistant", "content": "Hi there!"}
    # ]
    # await session.add_items(new_items)
    # items= await session.get_items()
    # print("All items are : ",items)
    
    # # last_item = await session.pop_item() #delete from the original array
    # # print("last item is : ",last_item)  
    
    # # items= await session.get_items()
    # # print("All items are : ",items)
    
    # user_input = str(input("Enter your Query here : "))
    # result = await Runner.run(agent, user_input, run_config=config, session=session)
    # print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    