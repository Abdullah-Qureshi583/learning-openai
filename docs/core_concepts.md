# What is OpenAI?

## OpenAI is an AI research and deployment company that creates powerful artificial intelligence models, tools, and APIs.

# Why Use OpenAI?

OpenAI provides some of the most advanced language models available today, like GPT-4 and GPT-4o. These models are known for their high accuracy, reliability, and strong reasoning ability. Developers choose OpenAI because it offers a well-documented API, robust performance, support for multiple modalities (text, image, audio), and powerful features like function calling, tool use, and memory. It’s trusted by many companies in production environments, which makes it a reliable choice when building serious AI applications.

---

# Why Use Other Models with the OpenAI SDK?

You use other models with the OpenAI SDK to take advantage of different strengths, costs, or features offered by those models—while keeping your code consistent and unified through a single SDK.

---

# How to Find the Exact Model Name?

The model names are listed in the **official documentation** of the provider you're using.  
For example:

- If you're using **Gemini**, check the [Gemini Docs](https://ai.google.dev/gemini-api/docs).
- If you're using **OpenAI**, visit [OpenAI's official models list](https://platform.openai.com/docs/models).

---

# How Do We Know What is the Exact Base URL?

We can get the exact base url from their official docs like for Gemini base URL we can get it from the **official Gemini API documentation**:  
📎 [Gemini OpenAI-Compatible API](https://ai.google.dev/gemini-api/docs/openai)

Example:

```python
base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
```
