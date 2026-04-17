# Incremental Index Updates in RAG

To perform **incremental index updates** in Retrieval-Augmented Generation (RAG), you must implement a strategy that detects and processes only the changes in your data source — additions, modifications, or deletions — rather than rebuilding the entire vector index from scratch.

## Core Strategies for Incremental Updates

### 1. Content Hashing & Tracking

- **Record Manager**: Use a persistent ledger, like LangChain’s `SQLRecordManager`, to track the hash of every document in your index.
- **Change Detection**: When syncing data, generate a hash (e.g., MD5) of the document content. Compare it to the stored hash to see if the file has changed.
- **Action Logic**:
  - **New**: Content doesn't exist → chunk, embed, and add.
  - **Changed**: Hashes differ → delete old embeddings and insert new ones.
  - **Deleted**: Document missing from source → remove associated vectors.

### 2. Vector Database "Upsert"

- Many vector databases (e.g., Pinecone, Milvus, Weaviate) support an **upsert** operation, which updates an existing vector if the unique ID matches or creates a new entry if it doesn't.
- Using a document key or metadata ID as the primary key ensures that updates target the correct entries without duplication.

### 3. Chunk-Level Management

- For large documents, tracking updates at the **chunk level** is more efficient. If only one section of a 50-page document changes, only the affected chunks need to be re-embedded.
- Tools like LlamaIndex provide methods like `refresh_ref_docs` to automatically handle these granular updates.

## Implementation Workflow

| Step | Action                  | Description |
|------|-------------------------|-----------|
| 1    | **Detect Change**       | Use file watchers, database logs, or event-driven triggers (like S3 events) to identify new or altered files immediately. |
| 2    | **Hash Fingerprinting** | Generate a unique hash for each document. Store it alongside a `source_id` in a tracking database (SQLite/PostgreSQL). |
| 3    | **Filter / Comparison** | Compare current source hashes against your tracking ledger. Skip unchanged files to save on embedding API costs and compute. |
| 4    | **Process Incremental** | For changed items: retrieve old IDs, delete them from the vector store, re-chunk the new text, generate new embeddings, and insert. |
| 5    | **Cleanup / Pruning**   | If a source document is deleted, ensure your indexing logic triggers a removal of all related chunks/vectors from the store. |

## Advanced Options

- **Integrated Vectorization**: Platforms like Azure AI Search offer built-in indexers that can be scheduled to periodically scan for changes and update the index automatically.
- **Incremental Graph Updates**: In specialized systems like GraphRAG, you can append new content by adding entities to existing communities instead of recomputing the entire knowledge graph.
