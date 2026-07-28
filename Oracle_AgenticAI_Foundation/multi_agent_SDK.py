import httpx
import truststore
ctx = truststore.SSLContext()

from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    function_tool,
    InputGuardrail,
    GuardrailFunctionOutput,
    input_guardrail,
    WebSearchTool,
)

ORDERS_DB = {
    "ORD-001":{"item":"Cricket bat","status": "shipped","eta": "March 20"},
    "ORD-002":{"item":"Python prograaming book","status": "Delivered","eta": "March 16"},
    "ORD-003":{"item":"usbc cable ","status": "processing","eta": "March 26"},
}

@function_tool ##tool decorator
def lookup_order(order_id: str) -> str:
    """Lookup the status of the customer oder by order id (eg., ORD-001)"""
    order=ORDERS_DB.get(order_id.upper())
    if order:
        return (
            f"Order {order_id.upper()}:\n"
            f" Item: {order['item']}\n"
            f" Status: {order['status']}\n"
            f" Estimated Arrigal: {order['eta']}"
        )
    return f"Order {order_id} not found, please enter a differnt order"

@function_tool
def process_refund(order_id: str) -> str:
    """Process a refunt request for a given order ID wih a reason."""
    order=ORDERS_DB.get(order_id.upper())
    if not order:
        return f"Cannot process refund: Order {order_id} not found"
    if order ["status"] == "Processing":
        return f"refund for order {order_id} cannot be processed  Order hasnt ben shipped yet"
    return (
        f" Refund initiated for oder {order_id.upper()} \n"
        f" Item: {order['item']}\n"
        f" Reason: {order['reason']}\n"
        f" Refund amount will be creditted in 7-4 days"
    )
class SupportCheck(BaseModel):
    is_support_question:bool
    reasoning: str

guardrail_checker = Agent(
    name="Support Topic Checker",
    instructions="""Determin if the user's message is a customer suport question.
    Valid topics: order status, refunts, return,s product questions, shipping, FAQs
    Invalid topics: Personal advice, okes, codeing help, unrelated conversations.
    Return is_support_question=True ONLY for customer support topics.""",
    output_type=SupportCheck,
    model="gpt-5.5",
)

@input_guardrail
async def support_only(ctx, agent, input):
    """Only allow customer support questions"""
    result = await Runner. run(guardrail_checker, input, context=ctx.context)
    final =result.final_output_as(SupportCheck)
    return GuardrailFunctionOutput(
        outputinfo={"reasoning": final.reasoning},
        tripwire_triggered=not final.is_support_question,
    )

order_agent = Agent(
    name="Order_status_Agent",
    handoff_description="Handles questions about order status, shipping, and delivery.",
    instructions="""Your help customers check their oder status
    Use the lookup_order tool to find order information.handoffs
    If the customer does not provide an order ID, ask for it
    Be friendly and professional""",
    tools=[lookup_order],
    model="gpt-5.5",
)

refund_agent = Agent(
    name="Refund_Agent",
    handoff_description="Hndles refund requests, returns, and cancellations",
    instructions="""Your help customers with refunds and returns.
    Use the process_refund tool to initiate refunds.
    Always ask for it order ID and reason before processing.
    Be friendly and professional""",
    tools=[process_refund],
    model="gpt-5.5",
)

faq_agent = Agent (
    name="FAQ_Agent",
    handoff_description="Handles general product questions and frequently asked questions.",
    instructions="""You answer general customer questions and FAQs.
    Use web search when you need current information.
    Common Topics: shipping policies, return windows, product details
    Be helpful and concise""",
    tools=[WebSearchTool()],
    model="gpt-5.5",
)

triage_agent = Agent(
    name="Customer_Support_Triage",
    instructions="""You are the front-line customer support agent
    your job is to understand the customer issue and route them to the right specialist:
    - order status, shpiing, delivery questions -> Order Status Agent
    - Refund requests, returns, cancellations -> Refund Agent
    - General Questions, product info, FAQs -> FAQ Agent
    Be warm, prfessional, and route quickly.    """,
    handoffs=[order_agent,faq_agent,refund_agent],
    input_guardrails=[support_only],
    model="gpt-5.5",
)

async def handle_customer(message:str):
    """Process a customer message through the support system"""
    print(f"Customer:{message}")
    try:
        result = await Runner.run(triage_agent, message)
        print(f" {result.last_agent.name}: {result.final_output}")
    except Exception as e:
        print(f" Blocked: this Does not appear to be a support question")
        print ("=" * 70)
        print()
async def main():
        print ("=" * 70)
        print(" CUSTOMER SUPPORT AGENT SYSTEM -- DEMO")
        print ("=" * 70)
        print()
        #Test 1 
        await handle_customer("Where is my order ORD-001?")

##Calling the main function 
if __name__=="__main__":
    asyncio.run(main())