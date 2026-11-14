import json
import os
import sys
from pathlib import Path
from typing import Any
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_SCRIPT = str(
    Path(__file__).resolve().parent / "servers" / "travel_server.py"
)


def get_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "travel": {
                "command": sys.executable,
                "args": [SERVER_SCRIPT],
                "transport": "stdio",
                "env": {
                    **os.environ,
                    "PYTHONUNBUFFERED": "1",
                },
            }
        }
    )


async def load_travel_tools():
    client = get_mcp_client()
    return await client.get_tools()


async def call_travel_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """Invoke an MCP tool by name and return parsed JSON/dict output."""
    tools = await load_travel_tools()
    tool_map = {tool.name: tool for tool in tools}

    if tool_name not in tool_map:
        raise ValueError(
            f"MCP tool '{tool_name}' not found. Available: {list(tool_map.keys())}"
        )

    raw_result = await tool_map[tool_name].ainvoke(arguments)

    if isinstance(raw_result, str):
        try:
            return json.loads(raw_result)
        except json.JSONDecodeError:
            return {"raw": raw_result}

    if isinstance(raw_result, list) and raw_result and isinstance(raw_result[0], dict):
        text_block = raw_result[0].get("text")
        if isinstance(text_block, str):
            try:
                return json.loads(text_block)
            except json.JSONDecodeError:
                return {"raw": text_block}

    return raw_result