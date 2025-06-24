from fastapi import FastAPI
from langchain_core.tools import tool
from langchain_mcp_adapters.fastapi import tool_server

# Define your tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

# 👇 This must exist for uvicorn to find it!
app: FastAPI = tool_server([multiply])

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mathServer:app", host="127.0.0.1", port=8001)
