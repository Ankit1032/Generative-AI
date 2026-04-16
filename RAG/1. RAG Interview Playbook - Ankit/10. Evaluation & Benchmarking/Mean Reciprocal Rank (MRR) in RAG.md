# Mean Reciprocal Rank (MRR) in RAG

Mean Reciprocal Rank (MRR) is a ranking quality metric used to evaluate the retrieval component of a RAG (Retrieval-Augmented Generation) pipeline. It measures how effectively your system positions the **first relevant document** at the top of its search results.

## How MRR Works

MRR focuses exclusively on the position of the **first correct answer** or relevant document found for a query.

1. **Reciprocal Rank (RR) Calculation**:  
   For a single query, you find the rank (**rank**) of the first relevant document and take its inverse (**1/rank**).

   - If the first relevant document is at **Position 1**, RR = 1.0  
   - If it is at **Position 3**, RR = 0.333...  
   - If no relevant document is found in the top-K results, RR = 0

2. **Mean Calculation**:  
   To get the final MRR, you average these Reciprocal Rank scores across all test queries.

### Formula

$$
MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}
$$

where:
- $|Q|$ = number of queries
- $\text{rank}_i$ = position of the first relevant document for query $i$

## Why Use MRR in RAG?

- **Speed to Context**: It indicates how quickly the RAG system finds the necessary information to pass to the LLM.
- **Interpretability**: An MRR closer to **1.0** means the system consistently places the best information at the very top.
- **Ideal Use Case**: It is particularly effective for question-answering bots or lookup systems where **a single relevant context snippet** is enough to generate an accurate answer.

## Critical Limitations

While simple to use, MRR has two main drawbacks in RAG evaluation:

- **Ignores "The Rest"**: It does not care about any relevant documents after the first one. If your LLM needs multiple snippets (multi-hop reasoning), MRR won't capture if the subsequent required chunks are actually retrieved.
- **Binary Relevance**: It treats all relevant documents as equal, rather than scoring how "highly" relevant they are.

For a more comprehensive view, MRR is often paired with **Recall@K** (to see if all relevant chunks were found) or **nDCG** (to evaluate the quality of the entire ranked list).
