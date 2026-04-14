# Does Chroma Vector DB Support Native Hybrid Search?

**No**, Chroma Vector DB does **not** have inbuilt, native hybrid search (combining dense vector and keyword/BM25 search) in the same way Weaviate does. 

Chroma is optimized for simplicity and speed in prototyping, whereas Weaviate specializes in production-ready hybrid search.

## Key Differences

- **Weaviate**: Offers built-in hybrid search, combining dense vectors for semantic meaning with sparse vectors for exact keyword matching.

- **Chroma DB**: Focuses on pure vector similarity search and metadata filtering. While you can implement hybrid-like results by combining metadata filtering with embedding searches, it does **not** have a native "hybrid" query method.

For applications requiring strong keyword-plus-semantic hybrid search functionality, **Weaviate** is considered a more suitable option.

---

