import os
from dotenv import load_dotenv                    
from langchain.chat_models import init_chat_model 
from langchain.agents import create_agent          
from langchain.tools import tool                   

load_dotenv()


@tool # tells LangChain: "this is a function the agent can use"
def get_weather(city: str) -> str:
    """Get weather for a given city.""" # The docstring tells the AI what this function does
    return f"It's always sunny in {city}!"


model = init_chat_model( # Creates a connection to the AI
    "gemini-2.5-flash",           
    model_provider="google_genai",
    temperature=0.7, # (0 = exact, 1 = very creative)
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

print("\n TEST 1: Asking about weather")
print("User: What is the weather in sf?\n")

response = agent.invoke( 
    {"messages": [{"role": "user", "content": "What is the weather in Tokyo?"}]}
)

print("Agent:", response["messages"][-1].content)



print("\n TEST 2: Asking a general question")
print("User: What is Python programming language?\n") # the agent will not use the tool

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is Python programming language?"}]}
)

print("Agent:", response["messages"][-1].content)

print()
print("The basic agent is working")
print()
