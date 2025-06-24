import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import HumanMessage, AIMessage
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio

# async def main():
#     client=MultiServerMCPClient(
#         {
#             "math":{ 
#                 "command":"python",
#                 "args":["../mcp_servers/mathserver.py"], ## Ensure correct absolute path
#                 "transport":"stdio"
#             },
#             "weather":{
#                 "url":"http://127.0.0.1:8000",
#                 "transport":"streamable_http"
#             }
#         }
#     )

system_prompt = SystemMessage(
    content=(
        "You are a helpful assistant. Use tools only when explicitly necessary. "
        "For greetings, small talk, or casual inputs, do not use tools. "
        "Only use 'multiply' for math. Only use 'TavilySearch' for fact-based queries."
    )
)

load_dotenv()

# LLM
llm = ChatGroq(model="llama3-8b-8192")

# Tool: Tavily
tool = TavilySearch(max_results=2)

# Tool: Multiply
def multiply(a: int, b: int) -> int:
    """
    Multiplies two integers and returns the result.

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Product of a and b
    """
    return a * b

tools = [tool]

llm_with_tool = llm.bind_tools(tools)

# State class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Tool-calling Node
# def tool_calling_llm(state: State):
#     return {"messages": [llm_with_tool.invoke(state["messages"])]}
def tool_calling_llm(state: State):
    messages = state["messages"]

    # Inject system prompt only if not already present
    if not any(
        (isinstance(m, SystemMessage) or (isinstance(m, dict) and m.get("type") == "system"))
        for m in messages
    ):
        # If your messages are dicts:
        messages = [{"type": "system", "content": system_prompt.content}] + messages
        # OR if your messages are LangChain Message objects:
        # messages = [SystemMessage(content=system_prompt.content)] + messages

    return {"messages": [llm_with_tool.invoke(messages)]}

# Build the graph
memory = MemorySaver()
builder = StateGraph(State)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", "tool_calling_llm")
builder.add_edge("tool_calling_llm",END)
graph = builder.compile(checkpointer=memory)

# Store per-thread conversation history
chat_threads = {}

# Run chatbot
def chat_with_graph(user_input: str, thread_id: str = "default") -> str:
    # Get or create the chat history for this thread
    if thread_id not in chat_threads:
        chat_threads[thread_id] = []

    # Add user message
    chat_threads[thread_id].append(HumanMessage(content=user_input))

    # Invoke the graph with full message history
    config = {"configurable": {"thread_id": thread_id}}
    response = graph.invoke({"messages": chat_threads[thread_id]}, config=config)

    # Get last assistant response and store it
    assistant_msg = response["messages"][-1]
    chat_threads[thread_id].append(assistant_msg)

    return assistant_msg.content 