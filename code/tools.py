# # there are 3 type of tools
# # 1. hosted tools
# # 2. Function Tool
# # 3. Function as tool

# import json
# from typing_extensions import TypedDict, Any

# from agents import Agent, FunctionTool, RunContextWrapper, function_tool

# from agents import Agent, Runner, OpenAIChatCompletionsModel
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# import asyncio
# import os
# from agents.run import RunConfig

# load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL = "gemini-2.0-flash"

# client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model=MODEL,
#     openai_client=client
# )

# config = RunConfig(
#     model=model,
#     model_provider=client,
#     tracing_disabled=True
# )

    
# @function_tool  
# async def count_lines(file_name:str):
#     with open("result.py") as f:
#     print(f.read())

# async def main():   

   
#     agent = Agent(
#         name="Assistant",
#         tools=[count_lines],  
#     )

            
#     user_input = str(input("How can I help you? "))
#     result = await Runner.run(agent, input=user_input, run_config=config)

#     print("🟢Response:", result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())

# # context, dynamic instruction, prompt, session
# # pdf summerizer



def count_lines(file_name:str):
    with open("code/result.py", "r") as f:
        # data = 'some data to be written to the file'
        # f.write(data)
        lines = f.readlines()
        print(len(lines))
        
        
count_lines("a")