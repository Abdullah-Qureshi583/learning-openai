# Streamed Event Overview

## Basics

- When we **directly print the result**, we **do not get the `streamed_event`** property.
- If we **run with `stream=True`**, it creates a property called **`streamed_event`** which we can **iterate over**.

## `streamed_event` Property

This property contains different event types, such as:

1. `AgentUpdatedStreamEvent`
2. `RawResponsesStreamEvent`
3. `RunItemStreamEvent`
4. *(and more depending on the context)*

## How to Check Event Types

- Use the `type` property of the event object to identify which event it is.

### Handling `RawResponsesStreamEvent`

- If the type is `raw_response_event`, it may contain **output text from the agent**.
- Check it by verifying the event instance:
  
  1. If the object is an instance of `ResponseTextDeltaEvent`:
     - Output text is found in the **`delta`** key.
  
  2. If it is **not** an instance of `ResponseTextDeltaEvent`:
     - The **`delta` key will not be present**, meaning no agent output text is included.

