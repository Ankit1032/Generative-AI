# ANN Indexes in RAG (Retrieval-Augmented Generation)

In RAG (Retrieval-Augmented Generation), ANN (Approximate Nearest Neighbor) indexes are used to quickly find relevant data, balancing speed and accuracy.

Key types include:
- HNSW (hierarchical graph structures)
- IVF (cluster-based)
- Flat (brute-force)

These methods speed up similarity searches by minimizing computational complexity on large datasets.

---

## Primary Types of ANN Index in RAG

### 1. Hierarchical Navigable Small World (HNSW)
- Builds a multi-layer graph where nodes are connected based on proximity
- Highly efficient for fast, accurate search

### 2. Inverted File Index (IVF)
- Clusters vectors into smaller groups
- Searches only relevant clusters
- Significantly speeds up retrieval on massive datasets

### 3. Locality Sensitive Hashing (LSH)
- Uses hash functions to group similar vectors into buckets
- Restricts searches to similar items

### 4. Product Quantization (PQ) / IVF-PQ
- Compresses vectors into smaller codes
- Reduces memory usage and speeds up computations
- Often combined with IVF

### 5. Flat Index (Exhaustive / Brute-force)
- Not an approximation (exact search)
- Calculates distance between query and every document vector
- High accuracy but low speed
- Often used as a baseline

---

## Key Considerations

### Speed vs Accuracy Trade-off
- HNSW → High accuracy, higher memory usage
- IVF / PQ → Faster search, lower memory usage, slight accuracy loss

### Metric Types
- Cosine similarity
- Dot product
- Euclidean distance

### Parameters
- efConstruction (for HNSW)
- nlist (for IVF)

These parameters are crucial for tuning index quality.
