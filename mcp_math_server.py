"""
MCP Math Srver -- The tool provider
This server exposes the exact same tools that were hardcoded in the run_Agent.py. 

"""

from mcp.server.fastmcp import FastMCP
import math

##Create the MCP Server
mcp = FastMCP("Math")

##These are the same tools we used in the run_agent.py script. 

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together. Use for addition operations."""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together. Use for multiplication operations."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers together. Use for division operations."""
    return a / b

@mcp.tool()
def square_root(number: float) -> str:
    """Calcualte the square root of a number"""
    if number < 0:
        return "error: cannot take square root of a negative number"
    return str(math.sqrt(number))
##Run the server
##transport ="stio" means the server communicates via standard input output stdin/stdout
##The agent launches it as a subprocess.

if __name__ == "__main__":
    mcp.run(transport="stdio")