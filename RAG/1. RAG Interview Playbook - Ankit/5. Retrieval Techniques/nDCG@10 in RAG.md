# nDCG@10 in RAG

**nDCG@10** (Normalized Discounted Cumulative Gain at rank 10) is a critical metric for evaluating the **retrieval quality** of a Retrieval-Augmented Generation (RAG) system. While precision and recall simply check if relevant documents were found, nDCG@10 measures if the **most relevant** documents were ranked in the **top 10 positions**.

### Why nDCG@10 Matters for RAG
In a RAG pipeline, the LLM is provided with retrieved context to generate an answer. Because LLMs have limited context windows and can suffer from "lost in the middle" effects, the **order** of retrieved documents is vital.

*   **Position Sensitivity:** Higher-ranked documents (e.g., position #1) have a much greater impact on the final generated answer than lower-ranked ones.
*   **Graded Relevance:** Unlike binary metrics (relevant/not relevant), nDCG can account for **degrees of relevance**—for instance, a primary source is more valuable than a secondary one.
*   **Normalization:** It provides a score from **0 to 1**, where 1.0 represents a perfect ranking of the top 10 items, allowing you to compare performance across different datasets or queries.

### Core Components
The metric is calculated in three stages:

1.  **DCG (Discounted Cumulative Gain):** Sums the relevance scores of the top 10 results, applying a **logarithmic discount** (e.g., $1 / \log_2(\text{rank} + 1)$) so that relevance further down the list contributes less.
2.  **IDCG (Ideal DCG):** The DCG score if the system had returned the top 10 results in perfect order of relevance.
3.  **nDCG:** The ratio of **DCG / IDCG**.

### Implementation and Tools
*   **Frameworks:** You can evaluate your RAG pipeline's nDCG using libraries like [Scikit-learn](https://scikit-learn.org) or specialized LLM evaluation frameworks like [Ragas](https://ragas.io) and [Arize Phoenix](https://arize.com).
*   **Benchmark Datasets:** Common benchmarks for RAG retrieval often report nDCG@10, such as [MS MARCO](https://github.io) or [MTEB (Massive Text Embedding Benchmark)](https://huggingface.co).
