# 🧠 Context in SupportAgent Example

This document covers all context‑related points in the given code.

---

## 1. `UserContext` dataclass

### Definition

```python
from dataclasses import dataclass

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    def prev_item(self):
        ...
```

### Purpose

- Holds user-specific data (`uid`, `is_pro_user`)
- Includes methods (e.g. `prev_item()`) that use that data

### Why no `__init__`?

- `@dataclass` auto‑generates `__init__`, `__repr__`, etc.

---

## 2. `Agent[UserContext]`

### Syntax

```python
agent = Agent[UserContext](...)
```

### Meaning

- Declares that this agent expects a `UserContext` object
- Enables type checking and IDE autocomplete

### If removed

- Code may still run if you pass `context=` at runtime
- You lose type safety and clarity

---

## 3. Passing context at runtime

### How

```python
response = await Runner.run(
    agent,
    context=pro_user,
    run_config=config,
    input="Hello"
)
```

### What

- `context=` gives the agent its `UserContext` instance
- Agent uses this data to customize behavior

---

## 4. Accessing wrapped context

### Why `context.context`?

- The framework wraps your `UserContext` once more

### How to read data

```python
is_pro = context.context.is_pro_user
items = context.context.prev_item()
```

---

## 5. Quick Summary

| Concept            | Purpose                                                   |
|--------------------|-----------------------------------------------------------|
| `@dataclass`       | Simplifies class definition, auto‑generates `__init__`    |
| `UserContext`      | Stores user ID, pro status, methods like `prev_item()`    |
| `Agent[UserContext]` | Binds agent to that context type                         |
| `Runner.run(context=)` | Supplies the actual `UserContext` instance            |
| `context.context`  | Unwraps framework wrapper to access your data             |
