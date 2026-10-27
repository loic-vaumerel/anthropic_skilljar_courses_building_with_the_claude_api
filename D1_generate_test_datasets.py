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
        "max_tokens": 2000,
        "messages": p_messages,
    }
    if p_system_prompt:
        v_parameters["system"] = p_system_prompt
    if p_output_config:
        v_parameters["output_config"] = p_output_config
    v_message = v_client.messages.create(**v_parameters)
    return "".join(b.text for b in v_message.content if b.type == "text")

def generate_dataset():
    v_prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Each item is a task that
requires Python, JSON, or a Regex to complete.
The solution criteria are key criteria for evaluating the solution.

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code.

Please generate 3 tasks.
"""
    v_schema = {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"task": {"type": "string"}, "format": {"type": "string", "enum": ["json", "python", "regex"]}, "solution_criteria": {"type": "string"}},
                    "required": ["task"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["task", "format", "solution_criteria"],
        "additionalProperties": False,
    }
    v_messages = []
    add_user_message(v_messages, v_prompt)
    v_text = chat(v_messages, p_output_config={
        "format": {"type": "json_schema", "schema": v_schema}
    })
    return json.loads(v_text)["tasks"]

v_client = Anthropic()
v_model="claude-sonnet-5-5"
v_dataset = generate_dataset()
with open("dataset.json", "w") as f:
    json.dump(v_dataset, f, indent=2)
