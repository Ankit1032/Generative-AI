# Hybrid Search in Weaviate

## Overview
Yes, hybrid search is inbuilt in Weaviate. It natively combines keyword-based search (BM25) and semantic vector search within a single query to improve retrieval accuracy for Retrieval-Augmented Generation (RAG).

## How to Perform Hybrid Search in Weaviate

To use hybrid search for a RAG pipeline, follow these primary steps:

1. **Initialize the Hybrid Query**  
   Use the `.with_hybrid()` method (Python SDK) or the `hybrid` operator in GraphQL.

2. **Set the query Parameter**  
   Provide the natural language search string. Weaviate uses this same string for both the keyword (BM25) and vector components.

3. **Adjust the alpha Parameter**  
   This is a float between 0 and 1 that balances the search types:
   - `alpha = 0`: Pure keyword search (BM25)
   - `alpha = 0.5`: Equal weighting of keyword and vector search
   - `alpha = 1`: Pure vector search

4. **Choose a Fusion Type**  
   By default, Weaviate uses `rankedFusion` to merge and rank the results from both search methods.

5. **Integrate with RAG**  
   Pass the retrieved top results into your LLM prompt as context.  
   If using frameworks like LangChain, you can use the specialized `WeaviateHybridSearchRetriever` to automate this flow.

## Key Advantages of Weaviate's Inbuilt Hybrid Search

- **No Manual Vectorization**: If you use a vectorizer module (like `text2vec-openai`), Weaviate automatically converts your search query into a vector in the background.
- **Parallel Execution**: Weaviate runs both the BM25 and vector searches in parallel for high performance.
- **Sparse Vectors Not Required**: Unlike some other databases, you do not need to pre-generate or store separate sparse vectors. Weaviate calculates the BM25 scores on-the-fly using the inverted index.

---

## Hybrid Search with Weaviate Python Client (v4)

To perform hybrid search with the Weaviate Python Client (v4), you use the `.query.hybrid()` method. This allows you to combine keyword (BM25) and vector search in a single step.

### 1. Basic Hybrid Search Code

This example demonstrates a standard hybrid search where you balance between semantic and keyword results using the `alpha` parameter.

```python
import weaviate
import os

# Connect to Weaviate (v4 Client)
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")  # Required if using OpenAI vectorizers
    }
)

try:
    # 1. Get the collection
    questions = client.collections.get("JeopardyQuestion")

    # 2. Perform Hybrid Search
    response = questions.query.hybrid(
        query="food",        # Search string for both BM25 and vector components
        alpha=0.5,           # 0.0 = pure BM25, 1.0 = pure vector search
        limit=3              # Number of results to return
    )

    # 3. Process results
    for obj in response.objects:
        print(f"Result: {obj.properties['question']}")
        
finally:
    client.close()
```

### 2. Hybrid Search for RAG (Generative Search)

Weaviate also has inbuilt generative search capabilities. You can perform a hybrid retrieval and immediately pass those results to an LLM for RAG in one request.



```python
# Perform hybrid search and generate a summary based on results
response = questions.generate.hybrid(
    query="history of nutrition",
    alpha=0.75,              # Weighted slightly more toward vector search
    grouped_task="Summarize the key historical facts about nutrition from these results.",
    limit=5
)

# Access the generated text
print(response.generated)
```

### Key Parameters Explained

* alpha: Controls the weighting. Set alpha=0.5 for an equal balance of keyword precision and semantic meaning.
* fusion_type: By default, Weaviate uses rankedFusion. You can also use relativeScoreFusion for different ranking logic.
* vector: Optional. If you already have a query vector (e.g., from a custom model), you can pass it manually alongside the text query.

For more advanced setups, you can explore the Hybrid Search Documentation or the Python v4 Client Reference for detailed API signatures.



