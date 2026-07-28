### test script to connect to oracle.oci-usage-mcp-server and list the available tools. 
##This call the tools from the MCP server writtin a seperate py script locally. 
# Creates an SSL Context using your native OS certificate chain
import httpx
import truststore
ctx = truststore.SSLContext()

##this is for reading files from OS
import os

## Async communication. 
import asyncio
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

##for laod environments from .env file
from dotenv import load_dotenv
load_dotenv()

##Importing the model from OpenAI
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

##This is the actual model defined. 
##model = init_chat_model("openai:gpt-4o-mini")
print("declaring the model")
model = ChatOpenAI(model="gpt-5.5", parallel_tool_calls=False)

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
print("defining the main function")
async def main():
    print("inside main function ")
    """
    Main async function -- MCP connections are async because they involve IO (Spawning processes, network calls)
    """
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # server_path = os.path.join(current_dir, "mcp_math_server.py")
    client = MultiServerMCPClient(
        {
            "oci_usage": {
                "command": "uvx",
                "args": ["oracle.oci-usage-mcp-server"],
                "transport": "stdio",
                "env": {
                    **os.environ,
                    "OCI_CONFIG_PROFILE":"DEFAULT",
                    "OCI_CLI_AUTO" : "api_key",
                    "FASTMCP_LOG_LEVEL": "ERROR",
                },
            },
        }
    )
    tools = await client.get_tools()
    print("=" * 55)
    print(" MCP Agent -- Tools discovered from MCP Server")
    print("=" * 55)
    print(f"\n Found {len(tools)} tools from MCP Server:\n")
    for t in tools:
        print(f" {t.name}: {t.description[:60]}...")
    print()

    agent = create_agent(
        model,
        tools=tools,
    )
if __name__ == "__main__":
    # asyncio.run(transport="stdio")
    asyncio.run(main())
