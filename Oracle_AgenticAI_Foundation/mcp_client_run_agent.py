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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "mcp_math_server.py")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [server_path],
                "transport": "stdio",
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

    async def run_agent(question: str):
        """Run the agent and prin the exection trace."""
        print(f" Usr: {question}")
        print("-" * 50)
        result = await agent.ainvoke({
        "messages": [("user", question)]
        })
        for msg in result ["messages"]:
            if msg.type == "human":
                continue
            elif msg.type == "ai":
                if msg.tool_calls:
                        for tc in msg.tool_calls:
                             print(f" Agent thinks -> calling: {tc['name']}(tc['args'])")
                elif msg.content:
                    print(f"Agent answer: {msg.content}")
            elif msg.type == "tool":
                 ##Extract clean result from MCP TOOL RESPONSE
                 content = msg.content
                 ##
                 ##
                 ##
                 if isinstance(content,list):
                    texts = [item["text"] for item in content if isinstance(item,dict) and "text" in item]
                    content = ",".join(texts) if texts else str(content)
                 print(f" Tool result: {content}")
        print("=" * 55)
        print()
    
    ##Test cases
    await run_agent("What is 23 + 44")    
    await run_agent("What is 15 multiplied by 8, and then divide the reulst by 3")
    await run_agent(
        "I have a rectable with width 12 and height 7"
        "What is the area, and what is the square root of that area"
    )
    #Edge case: error handling
    await run_agent("What is 100 divided by 0")
    await run_agent("What is square root of -22")

    print("")
    print()
    print("Key Take away")
    print("The MCP client server arch")
    print("!!!!")
##
##Calling the main function 
if __name__=="__main__":
    asyncio.run(main())