###tootls are hardcoaded in the script. 

print ("starting the script")
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
model = init_chat_model("openai:gpt-4o-mini")
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
import math
##Tool decorator
@tool
def add(a: float, b: float) -> float:
###Doc stirngs
    """Add two numbers together. Use for addition operations."""
### return type here its float
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together. Use for multiplication operations."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers together. Use for division operations."""
    return a / b
tools = [add, multiply, divide]
agent = create_agent(model=model,
                     tools=tools,)

def run_agent(question: str):
    """Run the agent and print the execution trace."""
    print(f"user:{question}")
    print("-" * 50)

    result = agent.invoke({
        "messages": [("user", question)]
    })
    print ("Agent:", result)

run_agent("What is 15 multiplied by 8, then divide the result by 3")