import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 1. Define how to spawn the server process
    server_params = StdioServerParameters(
        command="uvx",
        args=["oracle.oci-usage-mcp-server"],
        env={"OCI_CONFIG_PROFILE": "DEFAULT"}
      )

    # 2. Open standard input/output streams with the process
    async with stdio_client(server_params) as (read, write):
        # 3. Create the MCP ClientSession
        async with ClientSession(read, write) as session:
            # Initialize the MCP handshake protocol
            await session.initialize()

            # Discover available capabilities
            tools = await session.list_tools()
            print("Available Tools:", [tool.name for tool in tools.tools])

            # Call a specific tool provided by the server
            result = await session.call_tool("get_usage_summary", arguments={})
            print("Tool Output:", result.content)

if __name__ == "__main__":
    asyncio.run(main())