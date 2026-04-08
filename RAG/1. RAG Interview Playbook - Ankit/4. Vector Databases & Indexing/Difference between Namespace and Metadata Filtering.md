# Namespaces vs. Metadata Filtering in RAG

While both **Namespaces** and **Metadata Filtering** allow you to narrow down search results in a vector database, they function differently under the hood and serve different use cases.

### 1. Namespaces (Hard Partitioning)
Think of a namespace as a **separate folder** within your index. When you query a specific namespace, the database ignores everything outside of it entirely.

*   **Mechanism:** Physical or logical isolation of data at the storage level.
*   **Performance:** Very fast. The search space is strictly limited to the size of that namespace.
*   **Best Use Case:** **Multi-tenancy**. Use namespaces when you have strict data boundaries (e.g., User A must never see User B’s data).
*   **Limitation:** You typically cannot query across multiple namespaces in a single search.

### 2. Metadata Filtering (Soft Partitioning)
Metadata filtering is like using a **search filter** on a website. All data lives in the same space, but you apply rules (e.g., `category == 'legal'`) to hide irrelevant results after or during the search.

*   **Mechanism:** Attaching key-value pairs to vectors (e.g., `{"department": "HR", "year": 2023}`).
*   **Performance:** Slightly slower than namespaces on massive datasets because the engine may still need to scan the global index before applying the filter.
*   **Best Use Case:** **Granular categorization**. Use filtering when you need to combine multiple criteria (e.g., "Find docs where `author` is 'John' AND `date` is after '2022'").
*   **Limitation:** If a filter is too broad (e.g., filtering 90% of the database), it can lead to "search exhaustion" or high latency in some vector engines.

---

### Comparison Summary


| Feature | Namespaces | Metadata Filtering |
| :--- | :--- | :--- |
| **Analogy** | Different rooms in a house. | Different tags on a shared bookshelf. |
| **Isolation** | High (Hard boundary). | Moderate (Logical boundary). |
| **Query Flexibility** | One namespace at a time. | Combine multiple filters (AND/OR). |
| **Primary Goal** | Data separation & speed. | Search precision & flexibility. |

### Code Comparison (Pinecone/LangChain)

**Using a Namespace:**
```python
# Limits search strictly to "User-A" docs
docs = vectorstore.similarity_search(query, k=3, namespace="User-A")
```

**Using Metadata Filters:**
```python
# Searches the whole index but only returns "PDF" types from "2024"
filters = {"file_type": "pdf", "year": 2024}
docs = vectorstore.similarity_search(query, k=3, filter=filters)
```

