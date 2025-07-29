#  https://github.com/Abdullah-Qureshi583/learning-openai/blob/main/docs/context.md 
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool,RunContextWrapper
import asyncio
import os 
from dotenv import load_dotenv
from openai import AsyncOpenAI
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
    # By the use of BaseModel,we do not have to define the __init__ method
    # and we can use the attributes directly.
    # create the UserInfo class to represent user information structured
    class UserInfo(BaseModel):
        name: str
        uid: str
        password: str

    # if set the is_enabled to True, so that it will not passed to the LLM.
    # @function_tool(is_enabled=True) 
    
    # Define a function to fetch user age and mark it as a tool
    @function_tool()
    # this wrapper is just working normally as the parameter 
    # and by using this " RunContextWrapper[UserInfo] " we have just define the type, Nothing else.
    async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
        """Fetch the age of the user. Call this function to get user's age information."""
        # the return value will be passed to the LLM
        # and the LLM will use this value to generate the response.
        return f"The user {wrapper.context.name} is 47 years old"

    # Create the agent
    # and this part "[UserInfo]" is just to define the type of the context.
    agent = Agent[UserInfo](
        name="SupportAgent",
        # intructions are not necessary, but you can provide them if you want.
        instructions="You are helping a user. Fetch their age and provide personalized support.",
        tools=[fetch_user_age],
    )
    
    # Create a user context
    # and this context will be passed to the agent.
    user = UserInfo(uid="abdullah001", name="Abdullah Qureshi", password="securepassword123")
    
    # Run the agent with the user context
    # All the main works in the Runner when passing the context here 
    # Even we don't do any thing else so still the LLM will not able to access the context directly
    user_response = await Runner.run(agent,context=user, run_config=config, input="Hello what is my age?")
    print("⭕ User Response:", user_response)

if __name__ == "__main__":
    
    asyncio.run(main())


