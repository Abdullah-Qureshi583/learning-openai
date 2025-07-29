from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from pydantic import BaseModel
from agents.run import RunContextWrapper
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
    # Create a class to represent user context
    class UserContext(BaseModel):
        uid: str
        is_pro_user: bool = False

    def dynamic_instructions(context: UserContext, agent: Agent[UserContext]) -> str:
        is_pro_user = context.is_pro_user
        prev_items = context.prev_item()
        if is_pro_user:
            return f"You are helping a Pro user. Offer premium support and discounts. User previous items are: {prev_items} tell the user about their previous items and list previous items and discounts 50% for the next purchase. Stay professional and helpful."
        else:
            return f"You are helping a Free user. Just offer standard support. User previous items are: {prev_items} tell the user about their previous items and list previous items and discounts 20% fro the next purchase. Stay professional and helpful."

    agent = Agent[UserContext](
        name="SupportAgent",
        instructions=dynamic_instructions,  # 👈 we pass the function, not static text,
    )

    pro_user = UserContext(uid="abdullah001", is_pro_user=True)
    free_user = UserContext(uid="guest123", is_pro_user=False)

    response_pro = await Runner.run(agent,context=pro_user, run_config=config, input="Hello")
    response_free = await Runner.run(agent,context=free_user, run_config=config, input="Hello")
    
    print("🟢 Pro User Response:", response_pro)
    print("⭕ User Response:", response_free)

if __name__ == "__main__":
    asyncio.run(main())