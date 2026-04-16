# Retrieval-Augmented Generation (RAG) Evaluation

In Retrieval-Augmented Generation (RAG), evaluation is divided into **two core stages** — **Retrieval** (finding relevant information) and **Generation** (producing a response) — to pinpoint exactly where a system might be failing.

## 1. Retrieval Evaluation

This stage assesses the quality and relevance of the documents or text chunks fetched from the knowledge base in response to a user query.

### Key Metrics

- **Context Precision**: Measures the percentage of retrieved documents that are actually relevant to the query.
- **Context Recall**: Measures if the system captured all relevant documents available in the knowledge base.
- **MRR (Mean Reciprocal Rank)**: Evaluates how high the first relevant document appears in the ranked list.
- **NDCG (Normalized Discounted Cumulative Gain)**: Rewards systems that place the most relevant items at the top of the search results.
- **Hit Rate**: A binary metric checking if at least one relevant document appears in the top results.

## 2. Generation Evaluation

This stage measures how well the Large Language Model (LLM) uses the retrieved context to produce an accurate and helpful answer.

### Key Metrics

- **Faithfulness (or Groundedness)**: Measures if every claim in the generated response is strictly supported by the retrieved context, essentially checking for hallucinations.
- **Answer Relevancy**: Assesses whether the generated response directly and accurately addresses the user's initial question.
- **Answer Correctness**: Compares the generated answer to a "ground truth" or reference answer to measure factual similarity.
- **Traditional NLP Metrics**: Metrics like BLEU, ROUGE, and METEOR are sometimes used to measure linguistic similarity to a reference, though they are often considered less effective for LLMs than "LLM-as-a-judge" methods.

## Summary of the "RAG Triad"

A popular framework for evaluating RAG, often used by tools like Ragas and TruLens, focuses on **three critical relationships**:

1. **Context Relevance**: Is the retrieved context actually useful for the query?
2. **Faithfulness**: Is the answer derived only from the context?
3. **Answer Relevance**: Does the answer satisfy the user's prompt?

For automated testing, developers often use specialized libraries like **DeepEval** or **LangSmith** to run these evaluations at scale.
