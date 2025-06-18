import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    with open("eks.json", "r") as f:
        config = json.load(f)

    # Extract the EKS MCP server config
    server_config = config["mcpServers"]["awslabs.eks-mcp-server"]

    server_params = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"],
        env=server_config["env"]
    )

    # Connect to the EKS MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools_result.tools])

            # Call a tool (example)
            # result = await 
        session.call_tool("tool_name", arguments={})

if __name__ == "__main__":
    asyncio.run(main())