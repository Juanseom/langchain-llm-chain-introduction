# LangChain LLM Chain Introduction

This project shows how to build AI agents using **LangChain** and **Google Gemini** (free).

This project follows the official [LangChain Quickstart Tutorial](https://docs.langchain.com/oss/python/langchain/quickstart).

---

## Table of Contents
- [What is this project?](#what-is-this-project)
- [Project Architecture](#project-architecture)
- [What is LangChain?](#what-is-langchain)
- [What is an Agent?](#what-is-an-agent)
- [Components Explained](#components-explained)
- [Installation Instructions](#installation-instructions)
- [How to Run the Code](#how-to-run-the-code)
- [Example Output](#example-output)
- [Differences Between Scripts](#differences-between-basicagentpy-and-fullagentpy)

---

## What is this project?

This project has **two Python scripts** that show how to build AI agents step by step:

| File | What it does |
|------|-------------|
| `basic_agent.py` | A simple agent that answers questions and uses one tool |
| `full_agent.py` | A complete agent with memory, structured output, and multiple tools |

---

## Project Architecture

### File Structure

```
langchain-llm-chain-introduction/
│
├── basic_agent.py         # Simple agent with one tool
├── full_agent.py          # Complete agent with memory and structured output
├── requirements.txt       # Python dependencies
├── .env                   # API key
├── .env.example          # Template for .env file
├── .gitignore            # Files to ignore in Git
└── README.md             # This file
```

### Architecture Flow

```
User Question
     ↓
[ Agent ] ← System Prompt (instructions)
     ↓
[ Model ] ← AI (Gemini 2.5 Flash)
     ↓
Decision: Need a tool?
     ↓                    ↓
   YES                   NO
     ↓                    ↓
[ Tool Call ]         Direct Answer
     ↓
Get Result
     ↓
Format Response
     ↓
Return to User
```

---

## What is LangChain?

**LangChain** is a Python framework that makes it easy to build applications with AI models (like ChatGPT, Gemini, Claude, etc.).

It is like this:
- An AI model alone can only **answer questions**
- With LangChain, the AI can also **use tools**, **remember conversations**, and **respond in a specific format**

---

## What is an Agent?

An **agent** is an AI that can **think** and **act**:

1. It receives a question from the user
2. It **decides** if it needs to use a tool (function) to answer
3. If yes, it **calls the tool**, gets the result
4. It uses the result to give a **final answer**

Example:
```
User: "What is the weather in Tokyo?"
Agent thinks: "I need to use the get_weather tool"
Agent calls: get_weather("Tokyo")
Tool returns: "Sunny, 25°C"
Agent answers: "The weather in Tokyo is sunny and 25°C!"
```

---

## Components Explained

### 1. System Prompt
The system prompt is like a **job description** for the AI. It tells the AI what role it has and how to behave.

```python
SYSTEM_PROMPT = "You are an expert weather forecaster who speaks in puns."
```

### 2. Tools
Tools are **Python functions** that the agent can call. The AI reads the function name and description to know when to use each tool.

```python
@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"It's sunny in {city}!"
```

### 3. Model Configuration
We configure the AI model with settings like creativity level and response length.

```python
model = init_chat_model(
    "gemini-2.5-flash",            # Model name (Google Gemini)
    model_provider="google_genai",  # Provider
    temperature=0.7,                # Creativity (0=exact, 1=creative)
)
```

### 4. Structured Output
We can force the AI to respond in a **specific format** using a dataclass.

```python
@dataclass
class ResponseFormat:
    fun_response: str                      # Always required
    weather_conditions: str | None = None  # Optional
```

### 5. Memory
Memory lets the agent **remember** previous messages in the same conversation.

```python
checkpointer = InMemorySaver()
```

### 6. Agent Creation
We put everything together with `create_agent()`.

```python
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_weather],
    checkpointer=checkpointer,
)
```

---

## Installation Instructions

### Step 1: Prerequisites

- Python 3.10 or higher

### Step 2: Create a Virtual Environment

A virtual environment keeps your project dependencies isolated.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```


You should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Main framework
- `langchain-google-genai` - Google Gemini integration
- `langgraph` - For agent memory
- `python-dotenv` - For loading environment variables

### Step 4: Get Your Google API Key


1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Copy the key (it looks like: `AIzaSyC...`)

### Step 5: Configure the .env File

1. Open `.env`

2. Paste your API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. Save the file

---

## How to Run the Code

### Run the Basic Agent

```bash
python basic_agent.py
```

**What happens:**
1. The agent gets a question about weather
2. It calls the `get_weather` tool
3. It returns a formatted answer
4. Then it answers a general question without using tools

### Run the Full Agent

```bash
python full_agent.py
```

**What happens:**
1. The agent gets a question about "weather outside"
2. It calls `get_user_location` to find where the user is
3. It calls `get_weather_for_location` with that location
4. It returns a structured response with a pun
5. The user says "thank you"
6. The agent remembers the previous conversation and responds

---

## Example Output

### basic_agent.py

```
BASIC AGENT


--- Test 1: Asking about weather ---
User: What is the weather in Tokyo?

Agent: The weather in Tokyo is sunny and 25°C (77°F).

--- Test 2: Asking a general question ---
User: What is Python programming language?

Agent: Python is a popular programming language known for being easy to read...
```

### full_agent.py

```

FULL AGENT

--- Message 1: Asking about weather outside ---
User: What is the weather outside?

Agent response:
ResponseFormat(
    punny_response="Don't 'Florida' your chances of a good day, it's always sunny there!",
    weather_conditions="Sunny"
)

--- Message 2: Continuing the conversation ---
User: Thank you!

Agent response:
ResponseFormat(
    punny_response="You're welcome! I'm always here to weather your questions with a smile.",
    weather_conditions=None
)
```

---

## Differences Between basic_agent.py and full_agent.py

| Feature | basic_agent.py | full_agent.py |
|---------|---------------|--------------|
| Tools | 1 tool (weather) | 2 tools (weather + user location) |
| System Prompt | Simple | Detailed with instructions |
| Memory | No | Yes (remembers conversation) |
| Structured Output | No (free text) | Yes (ResponseFormat format) |
| Runtime Context | No | Yes (user_id) |
| Model Settings | Basic | Custom (temperature, timeout, max_tokens) |

---
