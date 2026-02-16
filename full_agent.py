
import os
from dataclasses import dataclass                          
from dotenv import load_dotenv                              
from langchain.agents import create_agent                   
from langchain.chat_models import init_chat_model           
from langchain.tools import tool, ToolRuntime               
from langgraph.checkpoint.memory import InMemorySaver      
from langchain.agents.structured_output import ToolStrategy 

load_dotenv()

# 1
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. 
If you can tell from the question that they mean wherever they are, 
use the get_user_location tool to find their location."""

# 2

@dataclass # simple way to define a data structure in Python.
class Context:
    """Custom runtime context schema."""
    user_id: str


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# 3

model = init_chat_model(
    "gemini-2.5-flash",            
    model_provider="google_genai",  
    temperature=0.7, # (0 = exact, 1 = very creative)
    timeout=30,                     
    max_tokens=1000, # length                
)

# 4

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None

# 5

checkpointer = InMemorySaver()

# 6

agent = create_agent(
    model=model,                                     
    system_prompt=SYSTEM_PROMPT,                     
    tools=[get_user_location, get_weather_for_location],  
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat), 
    checkpointer=checkpointer, 
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

print("\n MESSAGE 1: Asking about weather outside")
print("User: What is the weather outside?\n")

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

print("Agent response:")
print(response["structured_response"])


# we can continue the conversation using the same `thread_id`.
print("\n MESSAGE 2: Continuing the conversation")
print("User: Thank you!\n")

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Thank you!"}]},
    config=config,
    context=Context(user_id="1"),
)

print("Agent response:")
print(response["structured_response"])

print()
print("The full agent is working with memory and structured output.")
print()
