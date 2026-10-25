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

def chat(p_messages, p_system_prompt=None, p_temperature=1.0):
    v_parameters = {
        "model": v_model,
        "max_tokens": 1000,
        "messages": p_messages,
        "temperature": p_temperature
    }
    if p_system_prompt:
        v_parameters["system"] = p_system_prompt
    v_message = v_client.messages.create(**v_parameters)
    return "".join(b.text for b in v_message.content if b.type == "text")

v_client = Anthropic()
v_model="claude-sonnet-5-5"
# v_system_prompt = """
# You are an Python engineer who writes very concise code. Just answer with the function code and nothing else.
# """
v_messages = []
add_user_message(v_messages, "Generate a one sentence movie idea")
v_answer = chat(v_messages, p_temperature=0.0)
print(v_answer)

