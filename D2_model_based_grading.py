from dotenv import load_dotenv
from anthropic import Anthropic
from statistics import mean
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

def run_prompt(p_test_case):
    """Merge the prompt and test case input, then return the result"""
    v_prompt = f"""
Please solve the following task:

{p_test_case["task"]}
    """
    v_messages = []
    add_user_message(v_messages, v_prompt)
    v_output = chat(v_messages)
    return v_output

def grade_by_model(p_test_case, p_output):
    v_eval_prompt = f"""
You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{p_test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{p_output}
</solution>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
    """

    v_messages = []
    add_user_message(v_messages, v_eval_prompt)
    v_eval_text = chat(v_messages)
    return json.loads(v_eval_text)

def run_test_case(p_test_case):
    """Call run_prompt, then grade the result"""
    v_output = run_prompt(p_test_case)
    v_model_grade = grade_by_model(p_test_case, v_output)
    v_score = v_model_grade["score"]
    v_reasoning = v_model_grade["reasoning"]
    return {
        "output": v_output,
        "test_case": p_test_case,
        "score": v_score,
        "reasoning": v_reasoning,
    }

def run_eval(p_dataset):
    """Load the dataset and calls run_test_case with each case"""
    v_results = []
    for v_test_case in p_dataset:
        v_result = run_test_case(v_test_case)
        v_results.append(v_result)

    v_average_score = mean([v_result["score"] for v_result in v_results])
    print("-" * 100 + "\nAverage Score = " + str(v_average_score) + "\n" + "-" * 100)

    return v_results

v_client = Anthropic()
v_model="claude-sonnet-5-5"
with open("dataset.json", "r") as f:
    v_dataset = json.load(f)
v_results = run_eval(v_dataset)
print(json.dumps(v_results, indent=2))
