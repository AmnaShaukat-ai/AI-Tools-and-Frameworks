from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()


agent = Agent(
    "openai:gpt-4.1-mini"
)

@agent.tool_plain
def search_products(product_name : str) -> str:
    """ Search Products in the store"""

    if product_name == "iPhone 18 Pro Max":
        return "iPhone 18 Pro Max is available. Price 3500 AED"
    else: 
        return "Product not found."
    

@agent.tool_plain
def order_tracking(order_id : str) -> str:
    """ Track customer order """

    if order_id.upper() == "AB-105":
        return f"Order {order_id} is out for delivery"
    else:
        return "Order not found"

@agent.tool_plain
def check_inventory(product_name : str) -> str:
    """Check Product Stock in wearhouse."""

    if product_name == "iPhone 18 Pro Max":
        return "100 Units of iPhone 18 Pro Max available"
    
    else: 
        return "Stock Information not available for this product"


result = agent.run_sync(
    "is laptop available? how many units of laptop are available? and tell me order AB-105 status too."
)

print(result.output)