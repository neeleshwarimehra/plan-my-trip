
from langchain.mcp import MCPAdapter

from app.mcp.servers.travel_server import mcp as travel_mcp_server


async def get_travel_mcp_tools():
    """
    Discover available tools from the PlanMyTrip MCP server.
    """

    # async with MCPAdapter(travel_mcp_server) as adapter:
    async with MCPAdapter("http://127.0.0.1:8001/mcp") as adapter:
        tools = await adapter.list_tools()

    return tools


async def call_travel_mcp_tool(
    tool_name: str,
    arguments: dict,
):
    """
    Execute an MCP tool while its adapter connection is open.
    """

    async with MCPAdapter("http://127.0.0.1:8001/mcp") as adapter:
        tools = await adapter.list_tools()

        for tool in tools:
            if tool.name == tool_name:
                return await tool.ainvoke(arguments)

    raise ValueError(
        f"MCP tool '{tool_name}' was not found."
    )
