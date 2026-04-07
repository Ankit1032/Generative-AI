# Tiktoken

Tiktoken is a fast, open-source Byte Pair Encoding (BPE) tokenizer developed by OpenAI to convert text into tokens for their language models. It allows developers to estimate costs, manage context limits by counting tokens before API calls, and supports models like GPT-4o, GPT-4, and GPT-3.5-Turbo.

---

## Key Details About Tiktoken

### Purpose
- It breaks text down into smaller units (tokens) that LLMs understand.
- Common English text translates to roughly 
 of a word, or 100 tokens 
 75 words.

### Speed
- It is highly optimized for performance, making it efficient for large-scale applications.

### Encodings
- Different models use different encodings:

- o200k_base: Used for GPT-4o and GPT-4o-mini.
- cl100k_base: Used for GPT-4 and GPT-3.5-turbo.
- p50k_base: Used for Codex models.

### Usage
- It can be installed via pip install tiktoken and allows for encoding text to tokens and decoding tokens back to text.

---

## How it helps Developers

### Cost Estimation
- Because OpenAI charges based on token usage, tiktoken helps manage budget.

### Context Limit Management
- Ensures inputs do not exceed model capacity.
