# NDCG (Normalized Discounted Cumulative Gain) in RAG

NDCG (Normalized Discounted Cumulative Gain) is a **rank-aware metric** used to evaluate the retrieval stage of a RAG pipeline. It measures how well your system ranks relevant documents at the very top of its results list.

In RAG, since LLMs have limited context windows and can suffer from **"lost in the middle"** issues, ensuring the most useful information is in the first few positions is critical for accurate generation.

## How NDCG Works

NDCG works by rewarding systems for placing highly relevant results early and penalizing them when those same results are buried deep in the list. It is calculated in three steps:

1. **Cumulative Gain (CG)**:  
   This is the sum of the relevance scores of all retrieved items.  
   *Limitation*: It ignores the order. A relevant document at rank 10 gives the same score as one at rank 1.

2. **Discounted Cumulative Gain (DCG)**:  
   This adds a logarithmic penalty to the relevance scores based on their position. The further down a result appears, the less it contributes to the total score.

3. **Normalization (NDCG)**:  
   To make scores comparable across different queries (which might have different numbers of relevant documents), the DCG is divided by the **Ideal DCG (IDCG)** — the score achieved if the documents were perfectly ranked.  
   *Result*: A score between **0 and 1**, where **1** represents a perfect ranking.

## Why Use NDCG in RAG?

- **Positional Sensitivity**: It aligns with how LLMs process context; items at the beginning are often given more weight during generation.
- **Graded Relevance**: Unlike metrics like MRR (which only cares about the first "hit") or Recall (which treats all items equally), NDCG supports **multiple levels of relevance** (e.g., highly relevant = 3, partially relevant = 1, irrelevant = 0).
- **Reranking Evaluation**: It is the standard metric for evaluating **reranker models**, which are specifically designed to re-order retrieved chunks to put the best ones first.
