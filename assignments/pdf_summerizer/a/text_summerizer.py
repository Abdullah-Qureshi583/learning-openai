from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI
from dotenv import load_dotenv
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



agent = Agent(
    name="Helpful Assistant",
    instructions="You are a helpful assistant."
)

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session"""
    cl.user_session.set("history", [])
    
    
    elements = [
        cl.File(
            name="hello.py",
            path="./main.py",
            display="inline",
        ),
    ]

    await cl.Message(
        content="This message has a file element", elements=elements
    ).send()
    print(f"the elements are {elements} <==|")
    # await cl.Message(
    # content="Hello how can i help you today!").send()

@cl.on_message
async def main(message:cl.Message):
    """Handle incoming messages using Agent and Runner"""
    try:
        # send empty msg now
        msg = cl.Message(content="Analyzing...", author="AI Assistant")
        await msg.send()
        # Get conversation history
        history = cl.user_session.get("history", [])
        user_input = message.content
        
        # Add user message to history
        history.append({"role": "user", "content": user_input})
        
        # Run the agent with conversation history
        result = Runner.run_streamed(agent, input=history, run_config=config)
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







# import chainlit as cl
# from agents import Agent, Runner, OpenAIChatCompletionsModel
# from openai.types.responses import ResponseTextDeltaEvent
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
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

# agent = Agent(
#     name="Helpful Assistant",
#     instructions="You are a helpful assistant."
# )

# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("history", [])
#     await cl.Message(content="👋 Hello! You can send me a message or upload a file.").send()

#     # Ask for a file upload explicitly
#     files = await cl.AskFileMessage(
#         content="📂 Please upload a file (txt/pdf)...",
#         accept=[".txt", ".pdf"],
#         max_size_mb=5
#     ).send()

#     if files:
#         file = files[0]
#         cl.user_session.set("uploaded_file", file)  # save it in session
#         await cl.Message(content=f"✅ Received file: {file.name}").send()
#     else:
#         await cl.Message(content="⚠️ No file uploaded. You can still chat with me.").send()


# @cl.on_message
# async def main(message: cl.Message):
#     try:
#         msg = cl.Message(content="Analyzing...", author="AI Assistant")
#         await msg.send()

#         history = cl.user_session.get("history", [])
#         user_input = message.content
#         uploaded_file = cl.user_session.get("uploaded_file")

#         # Check if file exists
#         if uploaded_file:
#             # Access content as text
#             file_content = uploaded_file.content.decode("utf-8", errors="ignore")
#             user_input += f"\n\n(File content included)\n{file_content[:500]}"  # limit preview

#         # Add user input to history
#         history.append({"role": "user", "content": user_input})

#         result = Runner.run_streamed(agent, input=history, run_config=config)

#         streamed_text = ""
#         cursor = "|"
#         msg.content = cursor
#         await msg.update()

#         async for event in result.stream_events():
#             if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#                 streamed_text += event.data.delta
#                 msg.content = f"{streamed_text} {cursor}"
#                 await msg.update()

#         msg.content = streamed_text
#         await msg.update()

#         ai_output = result.final_output
#         history.append({"role": "assistant", "content": ai_output})
#         cl.user_session.set("history", history)

#     except Exception as e:
#         await cl.Message(content=f"❌ **Error:** {str(e)}").send()

