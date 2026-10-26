from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

################################################################################
# Context lost between the 2 requests
################################################################################

# v_client = Anthropic()
# v_model="claude-sonnet-5-5"
# v_message = v_client.messages.create(
#     model=v_model,
#     max_tokens=1000,
#     messages=[
#         {
#             "role": "user",
#             "content": "What is quantum computing? Answer in one sentence"
#         }
#     ]
# )
# print(v_message.content[0].text)

# v_message = v_client.messages.create(
#     model=v_model,
#     max_tokens=1000,
#     messages=[
#         {
#             "role": "user",
#             "content": "Write another sentence"
#         }
#     ]
# )
# print("-" * 100)
# print(v_message)

################################################################################
# Context kept between the 2 requests
################################################################################

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
    # return v_message.content[0].text # fails on 2nd call as content[0] is a Thinking Block, The TextBlock is iun content[1]
    return "".join(b.text for b in v_message.content if b.type == "text")

v_client = Anthropic()
v_model="claude-sonnet-5-5"
v_messages = []
add_user_message(v_messages, "Define quantum computing in one sentence")
v_answer = chat (v_messages)
add_assistant_message(v_messages, v_answer)
add_user_message(v_messages, "Write another sentence")
v_answer = chat (v_messages)
add_assistant_message(v_messages, v_answer)
# print(v_answer)
print(v_messages)
