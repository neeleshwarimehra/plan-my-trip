import asyncio

from app.mcp.client import (
    get_travel_mcp_tools,
    get_mcp_tool_by_name,
)


async def main():

    print("\nConnecting to PlanMyTrip MCP...")

    tools = await get_travel_mcp_tools()

    print("\nDiscovered tools:")

    for tool in tools:
        print(f" - {tool.name}")

    print("\nTesting reusable tool lookup...")

    budget_tool = await get_mcp_tool_by_name(
        "estimate_budget_allocation"
    )

    result = await budget_tool.ainvoke({
        "total_budget": 50000,
        "travelers": 2,
        "days": 6,
        "currency": "INR",
    })

    print("\nBudget result:")
    print(result)

    print("\nMCP CLIENT TEST PASSED!")


if __name__ == "__main__":
    asyncio.run(main())
