# Metadata Filtering in RAG

Metadata filtering in Retrieval-Augmented Generation (RAG) is a technique used to narrow down the search space within a vector database before or after a semantic search. It allows you to retrieve documents based on structured attributes (like `year`, `category`, or `author`) in addition to their semantic relevance.

### How it Works
1.  **Add Metadata**: During the document ingestion phase, you attach key-value pairs (metadata) to each text chunk.
2.  **Filter Search**: When querying, you provide a "filter" object alongside your natural language query. The vector database first isolates the chunks that match your filter criteria and then performs the semantic similarity search only on that subset.

### Implementation with Code (LangChain & ChromaDB)
This example uses [LangChain](https://langchain.com) and [ChromaDB](https://trychroma.com), a popular combination for local RAG development.

```python
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. ADD METADATA: Create documents with custom tags
docs = [
    Document(
        page_content="The 2024 financial report shows a 10% growth.", 
        metadata={"year": 2024, "department": "finance"}
    ),
    Document(
        page_content="Marketing strategies for 2023 focused on social media.", 
        metadata={"year": 2023, "department": "marketing"}
    ),
    Document(
        page_content="Quarterly revenue for 2024 exceeded targets.", 
        metadata={"year": 2024, "department": "finance"}
    )
]

# Initialize embeddings and store documents in the vector database
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(docs, embeddings)

# 2. PERFORM FILTERED SEARCH: Query only for 2024 finance documents
query = "What was the growth?"
search_filter = {
    "$and": [
        {"year": {"$eq": 2024}},
        {"department": {"$eq": "finance"}}
    ]
}

# Retrieve results matching the filter
results = vector_store.similarity_search(query, k=2, filter=search_filter)

for doc in results:
    print(f"Content: {doc.page_content} | Metadata: {doc.metadata}")
```

### Key Benefits
*   **Accuracy**: Prevents "noisy" results from irrelevant years or departments from appearing in your top results.
*   **Efficiency**: Reduces the number of vectors the system needs to compare, which can speed up retrieval in very large datasets.
*   **Control**: Allows for strict business rules, such as "only search documents the user has permission to see".
