# HNSW (Hierarchical Navigable Small World) – Complete Explanation with Intuition and End-to-End Example

**HNSW (Hierarchical Navigable Small World)** graphs are a powerful graph-based index for **approximate nearest neighbor (ANN) search** in high-dimensional vector spaces. They power many vector databases (e.g., FAISS, Milvus, Pinecone, Qdrant) because they deliver excellent speed, high recall, and logarithmic scaling with dataset size.

HNSW solves the problem of finding the *k* most similar vectors to a query vector quickly, even when your dataset has millions or billions of high-dimensional embeddings (e.g., from text, images, or audio models). Exact search would be too slow (O(N) or worse), so HNSW trades a tiny bit of accuracy for massive speedups.

## Core Intuition: Small World + Hierarchy (Skip-List Style)

HNSW builds on two elegant ideas:

1. **Navigable Small World (NSW) graphs** (the "small world" part):  
   In a *small-world* graph, you can reach any node from any other in a small number of hops (logarithmic in N). It mixes **short-range links** (local neighbors) with **long-range links** (hubs or distant jumps).  
   Search is *greedy*: from the current node, always jump to the neighbor closest to your query. This naturally navigates high-dimensional space without getting stuck.

2. **Hierarchy** (the "hierarchical" part, inspired by skip lists):  
   Instead of one flat graph, HNSW creates **multiple layers** of NSW graphs.  
   - **Top layers** (coarse/global view): Very few points + long-range connections → you jump across the entire space quickly.  
   - **Bottom layer** (fine/local view): All points + short-range connections → you refine locally with high precision.  

   Search starts at the top (zoom-out / global navigation) and descends layer by layer (zoom-in / local refinement). This is exactly like using Google Maps: highways at the country level, then state roads, then city streets.

   **Why it works so well**: Each layer separates *distance scales*. Upper layers avoid evaluating tons of short links; lower layers only refine once you’re already close. The result is near-logarithmic search time with high recall.

## Key Parameters (and Their Intuition)

- **M**: Max number of neighbors (degree) per node *per layer* (typical: 5–48). Controls memory and quality. Higher M → better recall, more memory.
- **M_max0** (for layer 0): Usually ~2×M — bottom layer is denser.
- **efConstruction**: Candidate list size *during index building* (higher = better graph quality, slower build).
- **efSearch** (or ef): Candidate list size *during query* (higher = better recall, slower search).
- **m_L** (≈ 1 / ln(M)): Controls probability of a point appearing in higher layers (skip-list style).

## How Layers Are Assigned (Probabilistic, Skip-List Style)

When inserting a new vector **q**, its **maximum layer** *l* is sampled from a geometric distribution:

$$
l = \left\lfloor -\ln(U) \cdot m_L \right\rfloor \quad (U \sim \text{Uniform}(0,1))
$$

This ensures:
- Most points only appear in layer 0.
- Progressively fewer points in higher layers (exponential decay).
- The graph stays balanced automatically.

## End-to-End: Construction (Insertion)

HNSW builds **incrementally** — you insert vectors one by one (no need to shuffle data).

**INSERT(q)** (simplified high-level):

1. Sample the new point’s max layer *l*.
2. Start from the current global **entry point** (a node in the highest layer).
3. **Phase 1 (descent to insertion layer)**: For each layer *l_c* from top down to *l*+1:  
   Perform a fast greedy search (ef=1) to find the closest node in that layer → use it as entry for the next lower layer.
4. **Phase 2 (actual insertion)**: For each layer *l_c* from *l* down to 0:  
   - Run **SEARCH-LAYER** with ef = efConstruction to get candidate neighbors.  
   - Select the M closest (using a heuristic to keep degrees bounded).  
   - Add **bidirectional** edges between q and those neighbors.  
   - If any neighbor exceeds its degree limit, prune its farthest connection.
5. If q’s layer is higher than the current max, update the global entry point to q.

The core **SEARCH-LAYER** subroutine (greedy best-first search with candidate list) works as follows:

- Initialize: C = {ep}, W = {ep}, visited = ∅
- While |C| > 0:
  - c ← extract closest to q from C
  - if dist(c,q) > dist(furthest in W, q): break
  - for each neighbor e of c in layer l_c:
    - if e not visited:
      - add e to visited
      - update C and W (keep only ef closest)

## End-to-End: Search (Query)

**SEARCH(q, k, efSearch)**:

1. Start at the global **entry point** in the highest layer.
2. For each layer from top down to 0:  
   - Run **SEARCH-LAYER** starting from current best (ef=1 for upper layers, efSearch for layer 0).  
   - When you reach a local minimum (no closer neighbor), descend to the same node in the layer below.
3. At layer 0, return the top-*k* closest from the final candidate list *W*.

## Toy Example (End-to-End Walkthrough)

Imagine a tiny 2D dataset (6 points in clusters for intuition):

- Cluster 1 (near origin): A(0,0), B(1,1)
- Cluster 2 (far right): C(10,0), D(11,1)
- Cluster 3 (far up): E(0,10), F(1,11)

**Construction** (M=2, m_L≈0.5, efConstruction=4):

1. Insert A → becomes entry point, only in layer 0.
2. Insert B → assigned to layer 0 only → connects to A (closest).
3. Insert C → randomly assigned to layer 1 (rare) + layer 0.  
   - Top layer (1): greedy from A → finds C is far but connects (long-range link created).  
   - Layer 0: connects to nearest (A or B).
4. Continue for D, E, F.  
   - Higher layers end up with A and C as "hubs" (long jumps between clusters).  
   - Bottom layer 0 becomes densely connected locally within clusters + a few cross-cluster shortcuts.

**Query** for a vector Q near (0.5, 0.5) (should return A/B):

- Start at entry point (say A in layer 1).
- Layer 1: greedy → stays at A or jumps to C (but C is farther, so local min = A).
- Descend to layer 0 at A.
- Layer 0 (efSearch=6): explore neighbors of A → quickly finds B (very close), discards far points like C/D/E/F.
- Return top-2: A and B.

Total hops: ~3–5 evaluations instead of checking all 6 points. In a real million-point dataset, this scales to ~log(N) hops.

## Why HNSW Is So Effective

- **Complexity**: Construction O(N log N), search O(log N) per query (in practice near-constant for fixed recall).
- **Recall**: Tunable via efSearch/efConstruction — easily >95% with small ef.
- **Robustness**: Handles clusters, high dimensions, and non-uniform data well.
- **Incremental**: Add/delete points on the fly (deletions are trickier but supported in modern implementations).

HNSW beautifully marries graph navigation with hierarchical zooming, giving you fast, accurate vector search that feels almost magical in production. 

**Recommended starting parameters**: M=16, efConstruction=200, efSearch=100 for a good balance.


#### Link: https://redis.io/blog/how-hnsw-algorithms-can-improve-search/
