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

def chat(p_messages, p_system_prompt=None, p_output_config=None):
    v_parameters = {
        "model": v_model,
        "max_tokens": 1000,
        "messages": p_messages,
    }
    if p_system_prompt:
        v_parameters["system"] = p_system_prompt
    if p_output_config:
        v_parameters["output_config"] = p_output_config
    v_message = v_client.messages.create(**v_parameters)
    return "".join(b.text for b in v_message.content if b.type == "text")

v_client = Anthropic()
v_model="claude-sonnet-5-5"
v_schema = {
    "type": "object",
    "properties": {
        "commands": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["commands"],
    "additionalProperties": False,
}

v_messages = []
v_prompt = """
Generate three different sample AWS CLI commands. Each should be very short.
"""
add_user_message(v_messages, v_prompt)
# v_text = chat(v_messages)
# print(v_text.strip())
v_text = chat(v_messages, p_output_config={
    "format": {"type": "json_schema", "schema": v_schema}
})

for v_command in json.loads(v_text)["commands"]:
    print(v_command)




# add_user_message(
#     v_messages,
#     "Generate a very short EventBridge rule as JSON. "
#     "Respond with only the JSON, no explanation."
# )
# v_text = chat(v_messages).strip()
# v_text = v_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
# print(json.loads(v_text))