# from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
# import asyncio
# from dataclasses import dataclass
# from pydantic import BaseModel
# import os 
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
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

# # # history_tutor_agent = Agent(
# # #     name="History Tutor",
# # #     handoff_description="Specialist agent for historical questions",
# # #     instructions="You provide assistance with historical queries. Explain important events and context clearly.",
# # # )

# # # math_tutor_agent = Agent(
# # #     name="Math Tutor",
# # #     handoff_description="Specialist agent for math questions",
# # #     instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
# # # )


# # # triage_agent = Agent(
# # #     name="Triage Agent",
# # #     instructions="You determine which agent to use based on the user's homework question",
# # #     handoffs=[history_tutor_agent, math_tutor_agent]
# # # )

# # # @function_tool
# # # def get_weather(city: str) -> str:
# # #     """returns weather info for the specified city."""
# # #     return f"The weather in {city} is sunny"


# # # agent = Agent(
# # #     name="Haiku agent",
# # #     instructions="Always respond in haiku form",
# # #     tools=[get_weather],
# # # )


# # # class CalendarEvent(BaseModel):
# # #     name: str
# # #     date: str
# # #     participants: list[str]

# # # agent = Agent(
# # #     name="Calendar extractor",
# # #     instructions="Extract calendar events from text",
# # #     output_type=CalendarEvent,
# # # )

# # # result = Runner.run_sync(agent, "at the day on 21 feb, abdullah qureshi was born and joined by nasir and ali",  run_config=config);
# # # print(result);



# @dataclass
# class UserContext:
#     uid: str
#     is_pro_user: bool
#     def prev_item(self):
#         return f"Previous item for {self.uid} are apple and banana"


# def dynamic_instructions(context: UserContext, agent) -> str:
#     print("Dynamic instructions called with context:", context)
#     print("Dynamic instructions called with agent:", agent)
#     if context.context.is_pro_user:
#         return "You are helping a Pro user. Offer premium support and discounts."
#     else:
#         return "You are helping a Free user. Just offer standard support."




# agent = Agent[UserContext](
#     name="SupportAgent",
#     instructions=dynamic_instructions,  # 👈 we pass the function, not static text
# )



# pro_user = UserContext(uid="abdullah001", is_pro_user=True)
# free_user = UserContext(uid="guest123", is_pro_user=False)


# response_pro = Runner.run_sync(agent,context=pro_user, run_config=config, input="am i a pro user? if yes, what are my previous items?")
# print("🟢 Pro User Response:", response_pro)

# # # Run for Free User
# # response_free = Runner.run_sync(agent, context=free_user,run_config=config, input="I need help")
# # print("🔵 Free User Response:", response_free)






from agents import Agent, Runner, OpenAIChatCompletionsModel
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
        name="Helpful Assistant",
        instructions="You are a helpful assistant.",
        
        
    )

    user_input = str(input("How can I help you? "))
    result = await Runner.run(agent, input=user_input, run_config=config)

    print("🟢Response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())