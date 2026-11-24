from pydantic import BaseModel, field_validator
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from pydantic_ai import UsageLimits

load_dotenv()

class Product(BaseModel):
    product : str
    price : float
    available : bool


item = Product(
    product = "Laptop",
    price = 2500, 
    available = True
)

class Event(BaseModel):
    title : str
    date : str
    time : str
    

product_agent = Agent(
    "openai:gpt-4.1-mini",
    output_type= Product,
)

# agent_result = product_agent.run_sync(
#     "Extract Product Details: Laptop price 2500 PKR and is available"
# )



@product_agent.tool_plain
def search_product(product_name : str) -> str:
    """ Search the Store and check product availability"""

    print("TOOL EXECUTED")

    if product_name.lower() == "laptop":
        return "Laptop is available"
    else:
        return "Product not Found"

tool_result = product_agent.run_sync(
    "Use search product to check whether Laptop is available"
)

print(tool_result.output)
print(tool_result.output.model_dump())


order_agent = Agent(
    "openai:gpt-4.1-mini",
     deps_type= str
)

@order_agent.tool
def track_order(ctx :RunContext[str]) -> str:
    """Track the customer's order"""

    order_id = ctx.deps

    return f"Order {order_id} is out for delivery"

order_result = order_agent.run_sync(
    "Where is my order?",
    deps = "ORD-101"
)

print(order_result.output)



event_agent = Agent(
    "openai:gpt-4.1-mini",
    output_type=Event
)

@event_agent.tool_plain
def create_event(title: str, date: str, time: str) -> Event:
    """Create an event with title, date and time."""

    return Event(
        title=title,
        date=date,
        time=time
    )

event_result = event_agent.run_sync(
    "Create an event titled Team Meeting on 25 November 2026 at 3 PM.",
    usage_limits=UsageLimits(request_limit=5)
)

print(event_result.output)


try:
    event = Event(
        title = "Property Viewing",
        date = "25 november 2026",
        time = "3:00 PM"
    )
    print("Event Created :", event)

except Exception as e:
    print("Validation Error :", e)
    print("Sorry booking failed please provide valid time.")


class Meeting(BaseModel):
    time : str

    @field_validator("time")
    @classmethod
    def check_time(cls, value):
        value = value.strip().upper()

        if value != "03:00 PM":
            raise ValueError("Meeting time must be 03:00 PM")
        return value 


meeting_agent = Agent(
    "openai:gpt-4.1-mini",
    output_type= Meeting,
    retries = 3
)

result = meeting_agent.run_sync(
    "Create a Meeting at 04:00 PM"
)

print(result.output)