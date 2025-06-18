import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create server parameters from your config
    server_params = StdioServerParameters(
        command="uvx",
        args=["awslabs.eks-mcp-server", "--allow-write"],
        env={
            "AWS_PROFILE": "default",
            "AWS_REGION": "us-west-2",
            "FASTMCP_LOG_LEVEL": "INFO"
        }
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools_result.tools])

            # Call a tool (example)
            # result = await session.call_tool("tool_name", arguments={})

if __name__ == "__main__":
    asyncio.run(main())