def strip_code_fence(p_text):
    v_text = p_text.strip()
    for v_prefix in ("```json", "```python", "```"):
        if v_text.startswith(v_prefix):
            v_text = v_text[len(v_prefix):]
            break
    if v_text.endswith("```"):
        v_text = v_text[:-3]
    return v_text.strip()

v_samples = [
    "```python\ndef f():\n    return 1\n```",
    "```json\n{\n  \"Version\": \"2012-10-17\"\n}\n```",
    "```\n^arn:aws:s3:::[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$\n```",
    "no fence here",
]
for v_s in v_samples:
    print(repr(strip_code_fence(v_s)))