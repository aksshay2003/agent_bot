from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather location"""
    return "Its raining in hyderabad"

if __name__=="__main__":
    mcp.run(transport="streamable-http")