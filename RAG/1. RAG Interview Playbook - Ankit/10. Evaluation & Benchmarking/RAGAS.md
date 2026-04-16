# Ragas: Retrieval-Augmented Generation Assessment

Ragas (Retrieval-Augmented Generation Assessment) is an open-source framework designed to evaluate RAG pipelines by measuring both the retrieval and generation components separately. It primarily works as a **"reference-free"** framework, meaning it leverages a strong Large Language Model (LLM) as a judge to evaluate your system's performance without requiring manually annotated ground-truth labels for most metrics.

## Core Evaluation Metrics (The "RAG Triad" + More)

Ragas breaks down evaluation into two distinct stages to pinpoint exactly where a pipeline might be failing.

### 1. Retrieval Metrics

These assess the quality of the context fetched by the search engine.

- **Context Precision**: Measures how relevant the retrieved items are. Ideally, only useful information should be retrieved, and it should be ranked higher in the results.
- **Context Recall**: Checks if the retriever actually found all the information required to answer the question, typically compared against a provided ground truth.
- **Context Entities Recall**: Verifies that all key entities (names, dates, places) from the ground truth are present in the retrieved context.

### 2. Generation Metrics

These assess the quality of the answer produced by the LLM based on the retrieved context.

- **Faithfulness**: Measures "grounding" — how much of the generated answer is derived directly from the retrieved context. This helps detect hallucinations.
- **Answer Relevancy**: Evaluates how well the answer addresses the user's actual question, ignoring factual accuracy and focusing on completeness and lack of redundancy.
- **Answer Correctness**: A combined end-to-end metric that factors in both factual accuracy (against ground truth) and semantic similarity.

## How the Evaluation Workflow Works

To run an evaluation, you typically need to prepare a dataset containing four fields: **Question**, **Answer**, **Contexts** (retrieved snippets), and optionally **Ground Truths**.

1. **Data Collection**: You run your RAG pipeline on a set of sample questions and record the generated response and the raw context chunks retrieved from your vector database.

2. **LLM-as-a-Judge**: Ragas calls a separate, typically more powerful LLM (like GPT-4) to act as a critic. For example, to measure Faithfulness, the judge breaks the answer into individual claims and cross-checks each one against the retrieved context.

3. **Scoring**: Each metric is calculated on a scale of 0 to 1, where 1 represents perfect performance.

4. **Synthetic Data Generation**: If you don't have a test set, Ragas can use an LLM to scan your documents and automatically generate a variety of complex question-and-answer pairs for you.

## Key Benefits

- **Actionable Insights**: By scoring retrieval and generation separately, you can tell if you need to improve your embedding model (retrieval issue) or your prompt/LLM choice (generation issue).
- **Automated Iteration**: It replaces slow and expensive human manual review with a consistent, repeatable automated loop.
