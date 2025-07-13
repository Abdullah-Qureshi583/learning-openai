# OpenAI Learning Exploration Notes

## Key Concepts to Explore

### 1. Handoffs
- Agent handoff mechanisms
- Multi-agent coordination

### 2. PPLX Online Search Tool
- Integration with PPLX
- Online search capabilities

### 3. Guardrails
- Safety and control mechanisms
- Content filtering and validation

### 4. Verbose Mode
- Enable traces for debugging
- Detailed logging and monitoring

## Learning Resources

### Effective Prompt Writing
- **Resource**: [Prompts by Examples](https://github.com/panaversity/learn-agentic-ai/tree/main/-01_lets_get_started/02_prompts_by_examples)
- Best practices for crafting effective prompts
- Real-world examples and templates

### Model Integration
- **OpenRouter Integration**: Connect with various models through OpenRouter
- Model selection and configuration

## Runner Class Methods

The Runner class provides different execution modes for agent interactions:

| Method | Sync vs Async | What It Does |
|--------|---------------|--------------|
| `run_sync(...)` | Synchronous | Blocks until the agent produces a reply |
| `run_async(...)` | Asynchronous | Returns a coroutine you await for the reply |
| `stream_sync(...)` | Sync streaming | Yields partial outputs as they arrive (blocking) |
| `stream_async(...)` | Async streaming | Async iterator over partial outputs (non-blocking) |

### Usage Notes
- **Synchronous methods**: Use when you need to wait for complete responses
- **Asynchronous methods**: Use for non-blocking operations and better performance
- **Streaming methods**: Use for real-time output display and user interaction 