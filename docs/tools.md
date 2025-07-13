# 🛠️ Tool Types & Agent Invocation Guide

A comprehensive guide to how agents interact with tools: the types of tools available, when they are called, and the logic behind their use or avoidance.

---

## 🔧 Tool Categories

### 1. **OpenAI-Hosted Tools (Paid)**

These are built-in tools provided by OpenAI, available to Pro users.

- **Web Search Tool**  
  Used to fetch real-time information from the internet.

- **File Search Tool** _(Low-cost)_  
  Allows semantic search across uploaded files (PDFs, DOCX, etc.).

- **Computer-Based Tools**  
  Perform system-level tasks such as:

  - Taking screenshots
  - Running scripts
  - Fetching device info (when permitted)

- **Image Generation Tool**  
  Generates or edits images based on user prompts using models like DALL·E.

---

### 2. **Custom Tools**

These are user-defined tools registered via function calling.

- **Python Functions**  
  These can:

  - Process data
  - Format responses
  - Fetch external API data
  - Trigger custom logic

- Any custom logic that returns structured output can be used as a tool.

---

### 3. **Agents as Tools**

An **agent** can itself be a tool. For example:

- A **specialized sub-agent** for customer support.
- A **multi-function orchestrator** acting as a meta-tool.

These are useful in hierarchical or multi-agent systems.

---

### ⚙️ Tool Invocation Requirement

> Tools must always be passed as an **array**, even if only one tool is available.

---

## ✅ When Tools Are Likely to Be Called

The agent uses a tool when:

- **🔍 Relevant Function Name**  
  The name closely matches the user's intent (e.g., `searchWeather` for "What's the weather?").

- **📄 Well-Written Docstring**  
  Descriptive, clear explanations in the docstring help agents choose the correct tool—even with vague names.

- **✅ Argument Compatibility**  
  The user's input can be mapped or converted into the expected argument type.

- **🧠 Few Tools Available**  
  If there are only a few tools, the agent is more likely to pick the closest match.

- **📚 Tool Usage History** _(for persistent agents)_  
  If a tool worked well previously in context, the agent may reuse it.

- **🧩 Fallback Exploration**  
  If the agent isn't sure how to respond, it may test a tool that has a weak match but might still be helpful.

---

## 🚫 When Tools Are Not Called

Tools are **skipped** when:

- **❌ Irrelevant Function Name**  
  A name that doesn't match user intent (e.g., `parseCSV` for a weather question).

- **❌ Poor or Missing Docstring**  
  Without clear description, the agent may ignore the tool—even if the name sounds promising.

- **🚫 Incompatible Argument Types**  
  If a tool expects a `List[int]` but the input is a `str`, and no coercion is possible, it won't be used.

- **🧩 Too Many Better Matches**  
  In a large toolset, only top matches are considered.

- **🛑 Missing Required Arguments**  
  If the agent can't guess or extract all required inputs, the tool is skipped.

- **🚧 Function is Marked as Deprecated or Experimental**  
  The agent deprioritizes or avoids tools with deprecation warnings in docstrings.

---

## ❌ When Tools Are Called but Results Are Ignored

Even when a tool is triggered, its result may be **discarded** if:

- **🎯 Output is Irrelevant**  
  The result doesn’t help answer the user's query.

- **🧾 Output Format is Unusable**  
  Long HTML blobs, poorly structured data, or raw error messages may be ignored or partially parsed.

- **🤖 Agent Already Knows the Answer**  
  If the agent can reason out the answer internally, it may ignore the tool’s result—even after invoking it.

- **💥 Error or Null Output**  
  The tool returns a broken or incomplete response (e.g., API failure, empty object).

---

## 📌 Behavior Summary Table

| Condition                              | Will Tool Be Used? | Notes                                          |
| -------------------------------------- | ------------------ | ---------------------------------------------- |
| Name & docstring are relevant          | ✅ Likely          | Strong match leads to invocation               |
| Argument types align or can be coerced | ✅ Likely          | Especially if simple types (str, int, list)    |
| Few tools available                    | ✅ Likely          | Less competition increases usage               |
| Name is vague or misleading            | 🚫 Unlikely        | Unless docstring is excellent                  |
| Missing required arguments             | 🚫 Not Called      | Agent avoids if it can't generate valid inputs |
| Output is irrelevant or noisy          | ❌ Ignored         | Agent may respond directly instead             |
| Agent already knows the answer         | ❌ Ignored         | Tool call was unnecessary fallback             |
| Output returns error/null              | ❌ Ignored         | Discarded and handled internally               |

---

## 📘 Best Practices for Tool Design

- ✅ Use **descriptive names** and **concise docstrings**.
- ✅ Accept **flexible argument types** where possible.
- ✅ Handle **null/error cases** gracefully and return structured errors.
- ❌ Avoid ambiguous function names like `doTask()` or `helperFunc()`.

---

🧠 **Use this guide as a reference** for designing, debugging, and improving tool invocation in agent-based systems.
