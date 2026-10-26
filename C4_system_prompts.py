from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

################################################################################
# v1 : always system prompt
################################################################################

# def add_user_message(p_messages, p_text):
#     v_user_message = {"role": "user", "content": p_text}
#     p_messages.append(v_user_message)

# def add_assistant_message(p_messages, p_text):
#     v_assistant_message = {"role": "assistant", "content": p_text}
#     p_messages.append(v_assistant_message)

# def chat(p_messages):
#     v_system_prompt = """
#     You are a patient math tutor.
#     Do not directly answer a student's questions.
#     Guide them to a solution step by step.
#     """
#     v_message = v_client.messages.create(
#         model=v_model,
#         max_tokens=1000,
#         messages=p_messages,
#         system=v_system_prompt
#     )
#     return "".join(b.text for b in v_message.content if b.type == "text")

# v_client = Anthropic()
# v_model="claude-sonnet-5-5"
# v_messages = []
# add_user_message(v_messages, "How do I solve 5x+3=2 for x?")
# v_answer = chat (v_messages)
# print(v_answer)

################################################################################
# v2 : system prompt or not
################################################################################

def add_user_message(p_messages, p_text):
    v_user_message = {"role": "user", "content": p_text}
    p_messages.append(v_user_message)

def add_assistant_message(p_messages, p_text):
    v_assistant_message = {"role": "assistant", "content": p_text}
    p_messages.append(v_assistant_message)

def chat(p_messages, p_system_prompt=None): 
    # Failing when p_system_prompt=None
    # v_message = v_client.messages.create(
    #     model=v_model,
    #     max_tokens=1000,
    #     messages=p_messages,
    #     system=p_system_prompt
    # )
    # Supporting when p_system_prompt=None
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
v_system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
v_messages = []
add_user_message(v_messages, "How do I solve 5x+3=2 for x?")
v_answer = chat(v_messages, v_system_prompt)
# v_answer = chat(v_messages)
print(v_answer)