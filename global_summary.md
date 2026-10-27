# 2_Anthropic overview

# Claude model family
*Source : claude_models_1.png*

## Notions
* Claude Opus
  * Highest level of intelligence
  * Cost: high
  * Latency: moderate
  * Supports reasoning
* Claude Sonnet
  * Balances quality, speed, cost
  * Cost: medium
  * Latency: fast
  * Supports reasoning
* Claude Haiku
  * Most cost-efficient, latency-optimized
  * Cost: low
  * Latency: fastest
  * No reasoning support

## Fundamental knowledges
* Opus best for
  * Advanced software development, large-scale architecting
  * Long-running tasks requiring sustained focus
  * Strategic planning, multi-step problem solving
  * Tasks benefiting from advanced reasoning
* Sonnet best for
  * Common coding tasks
  * Document creation and editing
  * Content marketing, copywriting
  * Data analysis and visualization
  * Image analysis
  * Process automation
* Haiku best for
  * Quick code completions and suggestions
  * Content moderation and filtering
  * Data extraction and categorization
  * Language translation
  * Q&A systems, knowledge retrieval
  * High-volume, straightforward text processing

## Key takeovers
* Only Opus and Sonnet support reasoning; Haiku does not

# Picking the right model
*Source : claude_models_2.png*

## Notions
* Claude Opus
  * Highly intelligent
  * More expensive
  * Higher latency
* Claude Sonnet
  * Strong balance of intelligence, cost and speed
* Claude Haiku
  * Moderate intelligence
  * Low cost
  * Highest speed

## Fundamental knowledges
* Spectrum: Intelligence (Opus) ↔ Cost/Speed (Haiku), Sonnet in between

## Key takeovers
* Trade-off: more intelligence = higher cost and latency
* Pick model by balancing intelligence vs cost/speed


# 3_Accessing Claude with the API

# Accessing the API
*Source : 01_Accessing the API.html*
* Notions
  * Request flow: client → your server → Anthropic API → model → server → client
  * Official SDKs: Python, TypeScript, JavaScript, Go, Ruby (or plain HTTP)
  * Required request fields: API key, model, messages, max_tokens
  * Processing stages: tokenization → embedding → contextualization → generation
  * Token: word, word part, space or symbol
  * Embedding: list of numbers representing a token's possible meanings
  * Contextualization: embedding refined using surrounding words
  * Generation: output layer gives next-token probabilities; mix of probability and controlled randomness; repeated token by token
  * Stop conditions: max_tokens reached, end-of-sequence token, stop sequence
  * Response: message, usage (input/output tokens), stop reason
* Fundamental knowledges
  * Never call the API from client-side code
  * API key stays on your server
  * Client talks to your server only
* Key takeovers
  * Exposed key = anyone can make unauthorized requests
  * Set token limits suited to the use case
  * Handle stop reasons in application logic

# Getting an API key
*Source : 02_Getting an API key.html*
* Notions
  * Keys created in the Anthropic Console (console.anthropic.com)
  * Key has a workspace (e.g. Default) and a name (to identify it)
* Fundamental knowledges
  * Steps: Console → Get API Keys → Create Key → workspace + name → copy key
* Key takeovers
  * Key is displayed only once; copy it immediately
  * Lost key: delete it and generate a new one

# Making a request
*Source : 03_Making a request.html*
* Notions
  * `client.messages.create()` is the core call
  * Parameters: `model`, `max_tokens`, `messages`
  * `max_tokens`: safety limit, not a target
  * Message = dict with `role` (`user` / `assistant`) and `content`
  * User message: human input; assistant message: Claude's output
* Fundamental knowledges
  * Setup: `pip install anthropic python-dotenv`
  * Key in `.env` as `ANTHROPIC_API_KEY`; `load_dotenv()`; `client = Anthropic()`
  * Text of the answer: `message.content[0].text`
  * Response object also holds metadata
* Key takeovers
  * Add `.env` to `.gitignore`
  * Keep key out of code and version control

# Multi-Turn conversations
*Source : 04_Multi-Turn conversations.html*
* Notions
  * Claude is stateless: stores no history, each request is independent
  * Conversation state is managed by your code
* Fundamental knowledges
  * Keep a `messages` list and send the full history with every request
  * Loop: send user message → append Claude's reply as assistant message → append next user message → resend all
  * Helpers: `add_user_message`, `add_assistant_message`, `chat`
* Key takeovers
  * Without history, follow-ups ("Write another sentence") lose context

# System prompts
*Source : 06_System prompts.html*
* Notions
  * System prompt: plain string guiding how Claude responds
  * Sets role, tone, style, approach
  * Claude answers as someone in that role would
  * Keeps Claude on task
* Fundamental knowledges
  * Passed via the `system` parameter of `create`
  * `system=None` is rejected by the API
  * Include `system` in params only when provided (`if system: params["system"] = system`)
  * Example: math tutor prompt → hints and guiding questions instead of direct answers
* Key takeovers
  * System prompts give consistent, role-appropriate behavior

# Temperature
*Source : 08_Temperature.html*
* Notions
  * Generation steps: tokenization → prediction (probabilities) → sampling
  * Temperature: value 0 to 1 adjusting selection probabilities
  * Low (near 0): deterministic, picks highest-probability token
  * High (near 1): probabilities spread out, more varied and creative
* Fundamental knowledges
  * Low 0.0–0.3: factual, coding, data extraction, content moderation
  * Medium 0.4–0.7: summarization, educational content, problem-solving, constrained creative writing
  * High 0.8–1.0: brainstorming, creative writing, marketing, jokes
  * Passed via `temperature` parameter in `create`; default 1.0 in course helper
* Key takeovers
  * Temperature changes likelihood of variety; it does not guarantee different outputs
  * Match temperature to use case

# Response streaming
*Source : 10_Response streaming.html*
* Notions
  * Problem: responses take 10–30 s, user sees only a spinner
  * Streaming: text arrives chunk by chunk within a single request
  * Events: MessageStart, ContentBlockStart, ContentBlockDelta, ContentBlockStop, MessageDelta, MessageStop
  * ContentBlockDelta carries the generated text
* Fundamental knowledges
  * Raw streaming: `stream=True` in `create`, iterate over events
  * Simplified: `client.messages.stream(...)` as context manager; iterate `stream.text_stream`
  * Full message after streaming: `stream.get_final_message()`
* Key takeovers
  * Server forwards chunks to client as they arrive → better UX
  * Use final message for database storage / further processing

# Structured data
*Source : 11_Structured data.html*
* Notions
  * Claude adds markdown fences and explanations by default
  * Prefilling: last message is an assistant message; Claude continues from it
  * Stop sequences: `stop_sequences=[...]` ends generation when matched
* Fundamental knowledges
  * Clean output = prefill the opening wrapper (e.g. "```json") + stop sequence on closing wrapper ("```")
  * Strip whitespace then parse: `json.loads(text.strip())`
  * Works for JSON, Python code, bullet lists, CSV
* Key takeovers
  * Identify what Claude naturally wraps content in; use it as prefill and stop sequence

# Quiz on accessing Claude with the API
*Source : 13_Quiz on accessing Claude with the API.html*
* Notions
  * Minimum request: API key, model, messages, max tokens
  * Claude doesn't remember previous messages
  * First processing step: tokenization
* Fundamental knowledges
  * Slow-feeling chat (long wait, then all text at once) → enable streaming
  * Math tutor giving hints → system prompt with the role
  * Predictable factual answers → low temperature (near 0.0)
  * Raw JSON only → prefilled message + stop sequences
* Key takeovers
  * API key lives on your server, never in client code


# 4_Prompt evaluation

# Prompt evaluation
*Source : 01_Prompt evaluation.html*
* Notions
  * Prompt engineering: techniques to write better prompts (multishot, XML tags, best practices)
  * Prompt evaluation: automated testing to measure prompt effectiveness
  * Eval uses: test against expected answers, compare prompt versions, review outputs for errors
  * 3 options after drafting a prompt
    * 1: test once → risky
    * 2: test a few times, fix corner cases → still misses unexpected inputs
    * 3: run an eval pipeline, score, iterate on metrics → most reliable (more work and cost)
* Fundamental knowledges
  * Users always give unexpected inputs in production
  * Eval gives objective metrics across many test cases
* Key takeovers
  * Catch problems in development, not in production
  * Engineers underestimate edge cases
  * Prefer option 3 for serious applications

# A typical eval workflow
*Source : 02_A typical eval workflow.html*
* Notions
  * 5 steps
    * Draft a prompt (baseline)
    * Create an eval dataset
    * Feed dataset inputs into the prompt → Claude responses
    * Grade responses
    * Change prompt and repeat
  * Dataset: sample inputs interpolated into the prompt template (tens to thousands of records)
  * Grader: scores question + answer, typically 1 to 10
  * Final score = average of scores (e.g. (10+4+9)/3 = 7.66)
* Fundamental knowledges
  * Dataset can be built by hand or generated by Claude
  * Same dataset must be reused to compare prompt versions
  * Many tools exist (open source and paid); start small, then scale
* Key takeovers
  * Objective score replaces guesswork
  * Iterate: higher average score = better prompt

# Generating test datasets
*Source : 03_Generating test datasets.html*
* Notions
  * Dataset = array of JSON objects (e.g. `{"task": ...}`)
  * Example use case: prompt generating Python, JSON or Regex for AWS tasks
  * Required output: clean code only, no explanation, header or footer
  * Prefill + stop sequence to get parseable JSON
    * `add_assistant_message(messages, "```json")`
    * `chat(messages, stop_sequences=["```"])`
* Fundamental knowledges
  * Use a faster model (Haiku) to generate test data
  * Dataset generation prompt: ask for short tasks solvable by a single function / object / regex
  * Save dataset to a file (`dataset.json`) for reuse
  * Helpers: `add_user_message`, `add_assistant_message`, `chat(messages, system, temperature, stop_sequences)`
* Key takeovers
  * Cheap model is enough for dataset generation
  * Persist the dataset so evals are repeatable

# Running the eval
*Source : 04_Running the eval.html*
* Notions
  * 3 core functions
    * `run_prompt(test_case)`: merge template + test case, call Claude, return output
    * `run_test_case(test_case)`: call `run_prompt`, then grade
    * `run_eval(dataset)`: loop over test cases, collect results
  * Result object: `output`, `test_case`, `score`
* Fundamental knowledges
  * Load dataset with `json.load`, then `run_eval(dataset)`
  * Score is hardcoded (10) until a grader is added
  * Full dataset run takes time (~30 s even with Haiku); optimize later
* Key takeovers
  * This pipeline is the core of most eval systems
  * Without format instructions, output is verbose
  * Grader is the missing piece

# Model based grading
*Source : 05_Model based grading.html*
* Notions
  * Grader: returns measurable feedback, typically 1 to 10
  * 3 grader types
    * Code graders: programmatic checks (length, words present/absent, JSON/Python/regex syntax, readability)
    * Model graders: another API call assesses quality, instruction following
    * Human graders: most flexible, slow and tedious
  * Evaluation criteria for code generation
    * Format: only Python/JSON/Regex, no explanation
    * Valid syntax
    * Task following
  * Format and syntax → code grader; task following → model grader
* Fundamental knowledges
  * Define criteria before building a grader
  * `grade_by_model` prompt asks for JSON: `strengths`, `weaknesses`, `reasoning`, `score`
  * Use prefill "```json" + stop sequence "```" to parse output with `json.loads`
  * Average with `statistics.mean` over all scores
* Key takeovers
  * Ask for strengths, weaknesses, reasoning with the score; otherwise models default to middling scores (~6)
  * Model graders are somewhat capricious but give a consistent baseline

# Code based grading
*Source : 06_Code based grading.html*
* Notions
  * Code grader checks format and syntax validity
  * Validators return 10 if parse succeeds, 0 if it fails
    * JSON: `json.loads`
    * Python: `ast.parse`
    * Regex: `re.compile`
  * Test cases need a `format` field (`python` / `json` / `regex`) to pick the validator
* Fundamental knowledges
  * Update dataset generation prompt to include `format`
  * Make prompt specific: respond only with Python, JSON or Regex; no comments or explanation
  * Prefill assistant with "```code" to get raw code
  * Combine scores: `(model_score + syntax_score) / 2`; weights adjustable
* Key takeovers
  * Code grader + model grader = full evaluation
  * Absolute score is not good or bad; what matters is improvement after prompt changes

# Quiz on prompt evaluation
*Source : 08_Quiz on prompt evaluation.html*
* Notions
  * Testing once → main risk: unexpected inputs break the prompt in production
  * Test case generation → use a faster model like Haiku
  * After generating responses → feed them to a grader
  * Measure real-world prompt performance → prompt evaluation methods
  * Model grader = grader using another AI model
* Fundamental knowledges
  * Ask for strengths, weaknesses and reasoning alongside the score to avoid mid-range scores
* Key takeovers
  * Result: 6/6


# 5_Prompt engineering techniques

# Prompt engineering
*Source : 01_Prompt engineering.html*
* Notions
  * Prompt engineering = improving a prompt for more reliable, higher-quality outputs
  * Iterative refinement process
  * Baseline = deliberately naive first prompt
  * Eval score (e.g. 2.3/10 baseline) + HTML report with grader reasoning
  * `PromptEvaluator`: `generate_dataset`, `run_evaluation`
  * `extra_criteria` = extra requirements for grader
* Fundamental knowledge
  * Cycle: set goal → write initial prompt → evaluate → apply technique → re-evaluate (repeat last two)
  * `max_concurrent_tasks`: start low (~3) to avoid rate-limit errors
  * 2-3 test cases in dev; more for final validation
  * `prompt_inputs_spec` defines the inputs the generated test cases must cover
* Key takeaways
  * Low initial score is normal
  * Change one thing at a time, measure impact, keep what works
  * Every technique must show measurable score improvement

# Being clear and direct
*Source : 02_Being clear and direct.html*
* Notions
  * Clear = simple language, state exactly what is wanted
  * Direct = instructions, not questions
* Fundamental knowledge
  * First line of the prompt is the most important
  * Start with an action verb (Write, Create, Generate, Identify)
  * Lead with the task, state key constraints
* Key takeaways
  * Treat Claude as a capable assistant needing clear direction
  * Example: "What should this person eat?" → "Generate a one-day meal plan for an athlete that meets their dietary restrictions" (2.32 → 3.92)

# Being specific
*Source : 03_Being specific.html*
* Notions
  * Output quality guidelines = length, structure/format, required elements, tone/style
  * Process steps = steps Claude must follow before answering
* Fundamental knowledge
  * Output guidelines: use in almost every prompt
  * Process steps: use for complex problems (troubleshooting, decisions, critical thinking, multiple angles)
  * Both are often combined
* Key takeaways
  * Specific guidelines give consistency and quality (3.92 → 7.86 in meal plan example)
  * Process steps ensure all factors are considered

# Structure with XML tags
*Source : 04_Structure with XML tags.html*
* Notions
  * XML tags = delimiters separating instructions from data and content types
  * Tag names are custom (no official tags required)
* Fundamental knowledge
  * Use when: large context/data, mixed content (code, docs, data), many interpolated variables
  * Descriptive names are better (`<sales_records>` > `<data>`)
  * Also useful for short content as delimiters
* Key takeaways
  * Value grows with prompt complexity and size
  * Reduces confusion between instructions and data

# Providing examples
*Source : 05_Providing examples.html*
* Notions
  * One-shot = one input/output example
  * Multi-shot = several examples covering different cases
* Fundamental knowledge
  * Use for: corner cases (e.g. sarcasm), complex output formats (JSON), style/tone, ambiguous inputs
  * Wrap in XML tags (`<sample_input>`, `<ideal_output>`)
  * Take top-scoring eval outputs (e.g. score 10) as examples
  * Explain why the example is ideal
  * Introduce with explicit text ("Here is an example input with an ideal response")
* Key takeaways
  * Show rather than tell
  * Target most common failure cases
  * Multi-shot for varied edge cases

# Quiz on prompt engineering techniques
*Source : 07_Quiz on prompt engineering techniques.html*
* Key takeaways
  * Best opening line: direct instruction ("Create a 30-minute workout plan for beginners")
  * Fix missed sarcasm: provide examples of sarcastic posts labeled negative
  * Prompt engineering = improving a prompt for more reliable, higher-quality outputs
  * Sample input/output pairs = one-shot / multi-shot prompting
  * XML tags purpose = structure and clarity with large content


