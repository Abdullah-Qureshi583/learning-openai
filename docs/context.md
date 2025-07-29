# 🧠 Context in OpenAI Agents SDK

> GitHub Path:  
> `https://github.com/Abdullah-Qureshi583/learning-openai/blob/main/code/context.py`


This document explains how context works in the `Agent[UserContext]` (now `Agent[UserInfo]`) system and how to use dynamic tools with user-specific data using `RunContextWrapper`.

---

## 1. `UserInfo` with `BaseModel`

### Definition

```python
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    uid: str
    password: str
```

### Purpose

- Holds structured user data (`name`, `uid`, `password`)
- Using `BaseModel` (from Pydantic) eliminates the need for a manual `__init__` method
- Attributes can be directly accessed and validated

---

## 2. `Agent[UserInfo]`

### Syntax

```python
agent = Agent[UserInfo](
    name="SupportAgent",
    instructions="You are helping a user. Fetch their age and provide personalized support.",
    tools=[fetch_user_age],
)
```

### Meaning

- Declares that this agent expects a `UserInfo` object as context
- Enables type safety and better autocomplete in IDEs
- Allows tools to access context data using the declared structure

---

## 3. Passing Context at Runtime

### How

```python
user = UserInfo(uid="abdullah001", name="Abdullah Qureshi", password="securepassword123")

response = await Runner.run(
    agent,
    context=user,
    run_config=config,
    input="Hello what is my age?"
)
```

### What It Does

- Supplies the actual context to the agent at runtime
- Ensures that the agent behaves based on this user information

---

## 4. Creating a Tool with Context Access

### Using `RunContextWrapper`

```python
from agents import function_tool, RunContextWrapper

@function_tool()
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"The user {wrapper.context.name} is 47 years old"
```

### Explanation

- The function is declared as a tool using `@function_tool()`
- The argument `wrapper: RunContextWrapper[UserInfo]` provides access to the user context inside the tool
- This tool can be used by the agent to fetch personalized data

---

## 5. Accessing Context Securely

- The context passed to the agent is not directly exposed to the LLM
- The LLM interacts with tools and receives processed responses (e.g., age string)
- This ensures sensitive data (like passwords) are not leaked unless explicitly returned

---

## 6. Complete Flow Summary

| Concept                       | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| `BaseModel`                   | Simplifies class creation and adds validation                          |
| `Agent[UserInfo]`             | Binds agent to structured context data                                 |
| `Runner.run(context=...)`     | Supplies context to the agent at runtime                               |
| `@function_tool()`            | Declares a function the agent can call                                 |
| `RunContextWrapper[UserInfo]`| Provides tool access to the context data securely                      |
| Tool Response                 | LLM sees the return value from the tool, not the full context directly |

---

## 7. Example Output

```text
⭕ User Response: The user Abdullah Qureshi is 47 years old
```

---

## 8. Source Code

View the full code here:  
📄 [context.md on GitHub](https://github.com/Abdullah-Qureshi583/learning-openai/blob/main/docs/context.md)

---
