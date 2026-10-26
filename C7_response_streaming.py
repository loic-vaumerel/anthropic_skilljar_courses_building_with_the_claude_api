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
# v1 : complete MessageStart / ContentBlockStart / ContentBlockDelta * x / Ends
################################################################################
# v_messages = []
# add_user_message(v_messages, "Write a one sentence description of a fake database")
# v_stream = v_client.messages.create(
#     model=v_model,
#     max_tokens=1000,
#     messages=v_messages,
#     stream=True
# )
# for v_event in v_stream:
#     print(v_event)

################################################################################
# v2
################################################################################
v_messages = []
add_user_message(v_messages, "Write a one sentence description of a fake database")
with v_client.messages.stream(
    model=v_model,
    max_tokens=1000,
    messages=v_messages,
) as v_stream:
    for text in v_stream.text_stream:
        print(text, end="")
    print()

print(v_stream.get_final_message())
