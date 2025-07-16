# Chainlit Quick Guide

## Setup
```bash
uv add chainlit openai python-dotenv agents
```

## Basic App Structure
```python
import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled=True)

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! How can I help?").send()

@cl.on_message
async def main(message: cl.Message):
    # Your AI logic here
    response = "Your response"
    await cl.Message(content=response).send()
```

## Run App
```
uv run chainlit run app.py
```

# Manage History in User Session
```python
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
     await cl.Message(
        content="How can I assist you today?"
    ).send()
```
```python
@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    user_input = message.content
    history.append({"role":"user", "content":user_input})
    result = await Runner.run(ai_agent, input = history)
    ai_output = result.final_output
    history.append({"role":"system", "content":ai_output})
    cl.user_session.set("history",history)
    await cl.Message(content= ai_output).send()
```

## OpenAI Integration
```python
# Direct OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = await client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": message.content}]
)

# Using Agents
provider = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = OpenAIChatCompletionsModel(model="gpt-3.5-turbo", openai_client=provider)
agent = Agent(name="Assistant", instructions="You are helpful", model=model)
result = await Runner.run_async(agent, message.content)
```


# Using Gemini with Agents
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)
agent = Agent(name="Gemini Assistant", instructions="You are helpful", model=model)
result = await Runner.run_async(agent, message.content)



## Streaming
```python
# Direct API streaming
msg = cl.Message(content="")
await msg.send()

stream = await client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[{"role": "user", "content": message.content}],
    stream=True
)

async for chunk in stream:
    if chunk.choices[0].delta.content:
        await msg.stream_token(chunk.choices[0].delta.content)

# Agents streaming (manual)
msg = cl.Message(content="")
await msg.send()

result = await Runner.run_async(agent, message.content)
response_text = result.final_output

for i in range(0, len(response_text), 10):
    chunk = response_text[i:i+10]
    await msg.stream_token(chunk)
    await asyncio.sleep(0.01)
```

## File Upload
```python
if message.elements:
    for element in message.elements:
        if isinstance(element, cl.File):
            # Process file
            pass
```

## Environment Variables (.env)
```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

## Agent Response Access
```python
# Get final output
response = result.final_output

# Get conversation history
history = result.conversation_history

# Get tool calls
tools_used = result.tool_calls
``` 