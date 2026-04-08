# Namespace in RAG

In Retrieval-Augmented Generation (RAG), a **namespace** is a logical partition within a vector database. It allows you to isolate different sets of data (vectors) within the same index, ensuring that queries only search through a specific subset of documents.

### Why use Namespaces?
*   **Multi-tenancy:** Isolate data for different users or customers to prevent cross-user data leaks.
*   **Organizational Clarity:** Separate data by category, such as "Support Docs" vs. "Legal Docs".
*   **Session Management:** Store individual user chat histories in separate namespaces for easy deletion or retrieval later.
*   **Environment Separation:** Keep "Development," "QA," and "Production" data distinct within one database instance.

### Code Example (Using Pinecone & LangChain)
The following Python example demonstrates how to "upsert" (upload) documents into a specific namespace and then query that same namespace to get relevant results.

```python
import os
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# 1. Initialize Pinecone and Embeddings
pc = Pinecone(api_key="YOUR_API_KEY")
embeddings = OpenAIEmbeddings()
index_name = "my-rag-index"

# 2. Uploading to a specific namespace ("user-123")
# This ensures these documents are isolated from other users
vectorstore = PineconeVectorStore.from_texts(
    texts=["Shipping takes 3-5 business days.", "Returns are accepted within 30 days."],
    embedding=embeddings,
    index_name=index_name,
    namespace="user-123"  # Data isolation starts here
)

# 3. Querying the same namespace
# If we don't specify the namespace, it will search the default (empty) namespace
query = "How long does shipping take?"
docs = vectorstore.similarity_search(
    query, 
    k=1, 
    namespace="user-123"  # Only searches inside "user-123"
)

print(docs.page_content)
# Output: "Shipping takes 3-5 business days."

## Key Differences

| Feature        | Without Namespaces                              | With Namespaces                              |
|----------------|--------------------------------------------------|----------------------------------------------|
| Search Scope   | Searches the entire index.                       | Searches only the specified partition.       |
| Security       | Harder to isolate private user data.             | Native support for multi-tenancy.            |
| Performance    | Slower retrieval as the database grows.          | Faster because it searches a smaller data subset. |
