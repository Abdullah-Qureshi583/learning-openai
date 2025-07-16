import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables and configure
load_dotenv()
set_tracing_disabled(disabled=True)

# Get API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
open_router_api_key = os.getenv("OPENROUTER_API_KEY")
# MODEL = "tngtech/deepseek-r1t2-chimera:free"
# MODEL = "deepseek/deepseek-chat-v3-0324:free"
# MODEL = "openai/gpt-4o-mini"
MODEL = "gemini-2.0-flash"

# Choose your provider - uncomment the one you want to use

# Option 1: Gemini (Google)
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Option 2: OpenRouter (uncomment to use)
# provider = AsyncOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=open_router_api_key,
# )

# Create model for agents
model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=provider
)

# Create the main AI agent
ai_agent = Agent(
    name="AI Assistant",
    instructions=(
        "You are a helpful AI assistant powered by advanced language models. "
        "Provide clear, accurate, and helpful responses. "
        "If files are uploaded, analyze them appropriately and provide insights. "
        "Be conversational, friendly, and professional in your responses."
    ),
    model=model
)

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    cl.user_session.set("history", [])
    await cl.Message(
    content="Hello how can i help you today!"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages using Agent and Runner"""
    try:
        # send empty msg now
        msg = cl.Message(content="Thinking...", author="AI Assistant")
        await msg.send()
        # Get conversation history
        history = cl.user_session.get("history", [])
        user_input = message.content
        
        # Add user message to history
        history.append({"role": "user", "content": user_input})
        
        # Run the agent with conversation history
        result = Runner.run_streamed(ai_agent, input=history)
        streamed_text = ""
        cursor = "|"  # Unicode block for a nice cursor effect
        msg.content = cursor
        await msg.update()
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                streamed_text += event.data.delta
                msg.content =f"{streamed_text} {cursor}"
                await msg.update()
        # Remove cursor at the end
        msg.content =streamed_text 
        await msg.update()      
        
        ai_output = result.final_output
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": ai_output})
        cl.user_session.set("history", history)
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Error:** {str(e)}\n\nPlease check your API configuration and try again."
        ).send()


