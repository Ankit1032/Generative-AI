from dotenv import load_dotenv
import os
from langchain.agents import create_agent

# Load .env variables
load_dotenv()

# Read API key
gpt_api_key = os.getenv("OPENAI_API_KEY")

# Set the environment variable that OpenAI expects
if gpt_api_key:
    os.environ["OPENAI_API_KEY"] = gpt_api_key
else:
    raise ValueError("GPT_API not found in .env file")

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response)