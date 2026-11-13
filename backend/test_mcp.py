import asyncio
from langchain.mcp import MCPAdapter

from app.mcp.servers.travel_server import mcp


async def main():
    async with MCPAdapter(mcp) as adapter:

        # Discover MCP tools
        tools = await adapter.list_tools()

        print("\n========== MCP DISCOVERED TOOLS ==========")

        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}\n")

        # Test budget tool
        budget_tool = next(
            tool for tool in tools
            if tool.name == "estimate_budget_allocation"
        )

        budget_result = await budget_tool.ainvoke({
            "total_budget": 50000,
            "travelers": 2,
            "days": 6,
        })

        print("\n========== BUDGET TOOL RESULT ==========")
        print(budget_result)

        # Test destination research tool
        research_tool = next(
            tool for tool in tools
            if tool.name == "get_destination_research_queries"
        )

        research_result = await research_tool.ainvoke({
            "destination": "Goa",
            "interests": ["beaches", "local food", "adventure"],
        })

        print("\n========== RESEARCH TOOL RESULT ==========")
        print(research_result)


if __name__ == "__main__":
    asyncio.run(main())
