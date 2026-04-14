The LangChain `EnsembleRetriever` is a search orchestration tool that combines multiple retriever algorithms—such as dense (semantic) and sparse (keyword) search—to improve document retrieval. It gathers results from multiple sources and ranks them using **Reciprocal Rank Fusion (RRF)**, ensuring high-quality, relevant context.

### What it is used for:

- **Hybrid Search**: Combining semantic similarity (e.g., Chroma, FAISS) with keyword-based search (e.g., BM25/Elasticsearch) to overcome the weaknesses of each. This ensures technical acronyms are found alongside conceptual meanings.
- **Improved RAG Performance**: In Retrieval-Augmented Generation (RAG) applications, it enhances context by merging results from different approaches, leading to better generative AI answers.
- **Weighted Ranking**: You can assign weights to different retrievers to prioritize one method over another (e.g., `weights=[0.5, 0.5]`).

### How it works:

1. **Input**: A query is passed to multiple retriever instances.
2. **Retrieve**: Each retriever identifies its top relevant documents.
3. **Merge & Rank**: The `EnsembleRetriever` uses Reciprocal Rank Fusion (RRF) to fuse these rankings, assigning higher priority to documents found consistently by multiple methods.

### Example Usage

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

# ... initialize sparse and dense retrievers ...

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_vectorstore.as_retriever()],
    weights=[0.3, 0.7]  # 30% weight to keyword, 70% to semantic
)

docs = ensemble_retriever.invoke("What is Hybrid Search?")