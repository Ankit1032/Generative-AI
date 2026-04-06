# Retrievers in RAG (Retrieval-Augmented Generation)

Retrievers in RAG (Retrieval-Augmented Generation) are mechanisms that fetch relevant context from knowledge bases, ranging from simple keyword searches to complex, specialized algorithms. Key types include Sparse (keyword), Dense (embedding-based), Hybrid, Parent Document, Multi-Query, and Knowledge Graph retrievers

---

## Detailed Breakdown of Retriever Types

### Naive/Vector Retriever
- Uses simple embedding-based similarity (cosine/distance) to find relevant document chunks, often using a standard embedding model.

### Sparse (Keyword-Based) Retriever
- Relies on traditional keyword searching techniques, such as the BM25 algorithm, to compute weighted word overlaps between the query and documents.

### Dense (Embedding-Based) Retriever
- Uses dense embeddings to capture semantic meaning rather than relying on exact keyword matches, creating a more semantic understanding of the query.

### Hybrid Retriever
- Combines both sparse (keyword) and dense (semantic) techniques, leveraging the strengths of both for improved retrieval accuracy.

### Parent Document Retriever (Small-to-Big Retrieval)
- Retrieves smaller child chunks for better embedding matching, but returns the larger parent document context to the generator, increasing the information available.

### Multi-Query Retriever
- Generates multiple variations of the user's query from different perspectives using an LLM to improve retrieval robustness and broaden the search.

### Contextual Compression Retriever
- Retrieves relevant documents and then immediately filters or summarizes them (compresses) to keep only the most relevant information.

### Self-Query Retriever
- Uses an LLM to analyze the prompt and convert it into structured queries to filter metadata alongside semantic search.

### Knowledge Graph Retriever
- Utilizes structured knowledge graphs to retrieve entities and their relationships, improving accuracy for complex, fact-dense queries.

### Ensemble Retriever
- Combines results from multiple different retrievers, often using algorithms like Reciprocal Rank Fusion to combine sparse and dense results.
