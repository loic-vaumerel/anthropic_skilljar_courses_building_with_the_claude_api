from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

def add_user_message(p_messages, p_text):
    v_user_message = {"role": "user", "content": p_text}
    p_messages.append(v_user_message)

def add_assistant_message(p_messages, p_text):
    v_assistant_message = {"role": "assistant", "content": p_text}
    p_messages.append(v_assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": v_model,
        "max_tokens": 1000,
        "messages": messages,
        "stop_sequences": stop_sequences,
        "extra_body": {"temperature": temperature},
    }

    if system:
        params["system"] = system

    message = v_client.messages.create(**params)
    return message.content[0].text

v_client = Anthropic()
v_model="claude-haiku-4-5"
# v_system_prompt = """
# You are an Python engineer who writes very concise code. Just answer with the function code and nothing else.
# """
v_messages = []
add_user_message(v_messages, "Generate a one sentence movie idea")
v_answer = chat(v_messages, temperature=1.0)
print(v_answer)

