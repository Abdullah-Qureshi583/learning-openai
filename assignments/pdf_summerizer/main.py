from agents import Agent, Runner, OpenAIChatCompletionsModel,enable_verbose_stdout_logging, function_tool
import time
from extract_pdf_text import extract_pdf_text
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import chainlit as cl
import asyncio
load_dotenv()
# enable_verbose_stdout_logging()

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



pdf_assistant = Agent(
    name="PDF Assistant",
    instructions="""
    You are a PDF specialist assistant. 
    - Use the `extract_pdf_text` tool whenever the user provides a PDF file or asks about its contents.  
    - Support tasks like extracting raw text, summarizing, answering questions about the document, or highlighting key sections.  
    - Do not handle general questions unrelated to PDFs. If the user asks about something else, let the main agent handle it.  
    - Beautify the return text.
    """,
    tools=[extract_pdf_text]
    
)

# General-purpose assistant
agent = Agent(
    name="Helpful Assistant",
    instructions="""
        You are a friendly and knowledgeable assistant.
        - If the user's query involves a PDF (upload, read, summarize, extract info, etc.),
        - Use the `extract_pdf_text` tool whenever the user asks about PDF file summary or its its contents.  
        - Support tasks like extracting raw text, summarizing, answering questions about the document, or highlighting key sections.  
        - Beautify the return text.
    """,
    handoffs=[pdf_assistant]
)


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session"""
    cl.user_session.set("history", [])
    await cl.Message(
        content="✨ Created by Abdullah Qureshi ✨"
    ).send()
    await cl.Message(
        content="✅ This is completely safe — don’t worry!"
    ).send()
    await cl.Message(
        content= "💬 Your data and chats are not being saved.  "
    ).send()


@cl.on_message
async def main(message:cl.Message):
    """Handle incoming messages using Agent and Runner"""
    try:
        # send Initial msg 
        msg = cl.Message(content="", author="AI Assistant")
        
        # Get conversation history
        history = cl.user_session.get("history", [])
                
        
        user_input =""
        
        if message.elements:
            for element in message.elements:
                # Check if the element is a file
                if isinstance(element, cl.File) and element.mime == "application/pdf":
                    user_input = f"""
                        The pdf name is :{element.name},
                        the pdf path is :{element.path},
                        {message.content}
                    """
                    msg.content ="Extracting pdf"
                    await msg.send()
                else:
                    await cl.Message(
                        content=f"⚠️ File not supported! Uploaded a PDF only. It's {element.mime}"
                    ).send()         
                    return       
        else:
            user_input = message.content
            msg.content ="Generating response"
            await msg.send()
        
        
            
        # Add user message to history
        history.append({"role": "user", "content": user_input})
        
        # Run the agent with conversation history
        result = Runner.run_streamed(agent, input=history, run_config=config)
        streamed_text = ""
        cursor = "|"  # Unicode block for a nice cursor effect
        
        
        
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                words = chunk.split(" ")
                for word in words:
                    streamed_text += word + " "
                    msg.content =f"{streamed_text} {cursor}"
                    await msg.update()
                
                    

        # Remove cursor at the end
        msg.content =streamed_text
         
        await msg.update()      
        print("The last agent is : ",result.last_agent.name)
        ai_output = result.final_output
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": ai_output})
        cl.user_session.set("history", history)
            
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Error:** {str(e)}\n\nPlease check your API configuration and try again."
        ).send()



@cl.on_stop
async def on_stop():
    pass

# @cl.on_message
# async def main(message: cl.Message):
#     # Check if there are any elements 
#     if message.elements:
#         for element in message.elements:
#             # Check if the element is a file
#             if isinstance(element, cl.File) and element.mime == "application/pdf":
#                 res = "< this the content >"
#                 # res = readPdf(element.path)
#                 await cl.Message(
#                     content=f"📄 You uploaded a PDF: {element.name} and the path is {element.path} \n the file content is : {res} and the user asking about : {message.content}  "
#                 ).send()
#             else:
#                 await cl.Message(
#                     content=f"⚠️ You uploaded a file, but it's not a PDF. It's {element.mime}"
#                 ).send()                
#     else:
#         # No files uploaded, just text
#         await cl.Message(
#             content=f"Received text: {message.content}"
#         ).send()
