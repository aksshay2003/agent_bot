
# 🤖 agent_bot

`agent_bot` is an intelligent assistant built using [LangGraph](https://github.com/langchain-ai/langgraph), designed to handle user queries with a combination of LLM-based reasoning and external tool usage like web search and arithmetic operations.

## ✨ Features
- 🧠 Powered by **LLaMA 3 (Groq)** via `ChatGroq`
- 🔍 Integrated **Tavily Search** tool for factual queries
- ➗ Built-in **Multiply Tool** for simple math
- 🧩 Modular graph-based reasoning using **LangGraph**
- 💬 Maintains multi-turn conversation history using `MemorySaver`

## 📁 Project Structure

```
agent_bot/
├── main.py                # Main agent orchestration logic (your shared script)
├── .env                   # Environment variables (LLM and Tavily API keys)
├── requirements.txt       # Python dependencies

```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/aksshay2003/agent_bot.git
cd agent_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
You'll need:
- `TAVILY_API_KEY` (from [Tavily](https://app.tavily.com/))
- `GROQ_API_KEY` (for using [Groq's LLaMA 3](https://console.groq.com/))

```env
TAVILY_API_KEY=your_tavily_key_here
GROQ_API_KEY=your_groq_key_here
```

## 🛠️ How It Works

- The user sends a message (e.g., `"What is the capital of France?"`).
- The message is passed to the LLM (`ChatGroq` with tools bound).
- The LLM chooses whether to:
  - Use the **TavilySearch** tool (for real-time facts),
  - Use the **Multiply Tool** (for math),
  - Or respond directly.
- All responses are tracked using `MemorySaver`, supporting multi-turn dialogue.

## 🧪 Example Usage

```python
from main import chat_with_graph

response = chat_with_graph("What's 7 * 8?")
print(response)  # Output: 56

response = chat_with_graph("Who is the President of the US?")
print(response)  # Output: (Uses TavilySearch to find the answer)
```

## 📦 Requirements

Here's a minimal example of your `requirements.txt`:

```
langchain
langgraph
langchain-core
langchain-tavily
langchain-groq
langchain-mcp-adapters
python-dotenv
typing-extensions
```

> ✅ Ensure your Python version is 3.9 or above.

## ❓ Notes

- This repo currently **ignores the `mcp_servers/`** directory as requested.
- You can re-enable multi-tool capabilities (e.g., weather/math servers) by uncommenting the `MultiServerMCPClient` portion.
- You can extend tools using LangChain’s tool interface or by adding your own functions.

## 📄 License

MIT License
