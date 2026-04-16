# Faithfulness vs Context Precision in RAG

In Retrieval-Augmented Generation (RAG), **Faithfulness** and **Context Precision** evaluate two different stages of the pipeline: the **generator** (how the LLM uses information) and the **retriever** (how well relevant information is found and ranked).

## Core Differences

| Feature              | Faithfulness (Groundedness)                          | Context Precision                                      |
|----------------------|-------------------------------------------------------|--------------------------------------------------------|
| **Focus**            | Evaluates the Generator (LLM)                        | Evaluates the Retriever (Search)                       |
| **Definition**       | Measures if the generated answer is factually consistent with the retrieved context | Measures if relevant information is ranked higher in the retrieved results |
| **Purpose**          | Prevents hallucinations                              | Ensures the LLM is fed the most useful info first      |
| **Relationship**     | Answer ↔ Context: Does the answer come only from the context? | Context ↔ Query: Are the top-ranked chunks actually relevant? |

## 1. Faithfulness (Groundedness)

This check ensures the LLM doesn't "invent" details not found in the documents.

**Query:** "Who founded OpenAI?"

**Retrieved Context:** "OpenAI was founded in 2015 by Sam Altman, Elon Musk, and others."

- **LLM Answer (Faithful):** "Sam Altman and Elon Musk founded OpenAI in 2015."  
  *(Score: High — all claims are in the context)*

- **LLM Answer (Unfaithful):** "Sam Altman founded OpenAI in San Francisco."  
  *(Score: Low — "San Francisco" is not in the context, even if true in reality)*

## 2. Context Precision

This evaluates the quality and order of the search results before the LLM even sees them.

**Query:** "What is the capital of France?"

**Retrieved Results (High Precision):**
1. "Paris is the capital of France." *(Relevant)*
2. "Lyon is a major city in France." *(Irrelevant)*

→ Relevant info is at the top.

**Retrieved Results (Low Precision):**
1. "French cuisine is world-famous." *(Irrelevant)*
2. "Paris is the capital of France." *(Relevant)*

→ The relevant chunk is buried below noise.

## Why Both Matter

- **Low Faithfulness + High Context Precision**: The retriever found the right info, but the LLM ignored it or hallucinated.
- **High Faithfulness + Low Context Precision**: The LLM is being "honest," but it's working with poorly ranked or noisy data, which might lead to incomplete answers.

Frameworks like **Ragas** and **DeepEval** provide automated ways to measure these using **"LLM-as-a-judge"** techniques.
