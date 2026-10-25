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

def chat(p_messages):
    v_message = v_client.messages.create(
        model=v_model,
        max_tokens=1000,
        messages=p_messages
    )
    return "".join(b.text for b in v_message.content if b.type == "text")

v_client = Anthropic()
v_model="claude-sonnet-5-5"
v_messages = []
while True:
    v_user_input = input("> ")
    if (v_user_input == "quit"):
        exit(0)
    # print(v_user_input)
    add_user_message(v_messages, v_user_input)
    v_answer = chat(v_messages)
    add_assistant_message(v_messages, v_answer)
    print("---")
    print(v_answer)
    print("---")
