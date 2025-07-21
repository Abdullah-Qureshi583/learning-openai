import chainlit as cl
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


@cl.on_chat_start
async def chat_start():
    """initialize the chat session"""
    cl.user_session.set("history",[])
    await cl.Message(content="How can i help you today?").send()



@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(content="", author="AI Assistant")
    await msg.send()
    
    history = cl.user_session.get("history",[])
    user_input = message.content
    
    history.append({"role":"user", "content":user_input})

    result = Runner.run_streamed(agent, input=history, run_config=config)
    streamed_text = ""
    cursor= "|"
    msg.content = f"{cursor}"
    await msg.update()
    async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                streamed_text += event.data.delta
                msg.content =f"{ streamed_text } {cursor}"
                await msg.update()
                
    msg.content= streamed_text
    await msg.update()
# asyncio.run(main())