from dotenv import load_dotenv
from anthropic import Anthropic
import os
import json

load_dotenv()

def add_user_message(p_messages, p_text):
    v_user_message = {"role": "user", "content": p_text}
    p_messages.append(v_user_message)

def add_assistant_message(p_messages, p_text):
    v_assistant_message = {"role": "assistant", "content": p_text}
    p_messages.append(v_assistant_message)

def chat(p_messages, p_system_prompt=None):
    v_parameters = {
        "model": v_model,
        "max_tokens": 1000,
        "messages": p_messages,
    }
    if p_system_prompt:
        v_parameters["system"] = p_system_prompt
    v_message = v_client.messages.create(**v_parameters)
    return "".join(b.text for b in v_message.content if b.type == "text")

v_client = Anthropic()
v_model="claude-sonnet-5-5"

################################################################################
# v1 : Not supported by the new models
################################################################################
# v_messages = []
# add_user_message(v_messages, "Generate a very short event bridghe rule as json")
# add_assistant_message(v_messages, "```json")
# v_answer=chat(v_messages, stop_sequences=["```"])
# print(json.loads(v_answer.strip()))

################################################################################
# v2 : Fixed by claude
################################################################################
v_messages = []
add_user_message(
    v_messages,
    "Generate a very short EventBridge rule as JSON. "
    "Respond with only the JSON, no explanation."
)
v_text = chat(v_messages).strip()
v_text = v_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
print(json.loads(v_text))