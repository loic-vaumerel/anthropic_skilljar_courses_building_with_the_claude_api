from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

# print(os.environ.get("ANTHROPIC_API_KEY"))
v_client = Anthropic()
v_model="claude-sonnet-5-5"
v_message = v_client.messages.create(
    model=v_model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)

print(v_message.content[0].text)