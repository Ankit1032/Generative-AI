# Fusion Methods in RAG

In Retrieval-Augmented Generation (RAG), **fusion methods** are techniques used to merge and re-rank document results from multiple sources (such as hybrid search or multiple query variations) into a single, optimized list for the Large Language Model (LLM).

Why do we need fusion?
Because no single retriever is perfect:

   - BM25 → good for keyword matching
   - Dense embeddings → good for semantic similarity
   - Hybrid systems → combine both

Fusion helps leverage strengths of all.

### 1. Reciprocal Rank Fusion (RRF)
**Definition**: RRF is a rank-based algorithm that calculates a score for each document based solely on its position in multiple retrieved lists, rather than the raw similarity scores.

*   **Explanation**: It uses a formula where the score is the sum of the reciprocal of each rank plus a constant $k$ (typically 60). This "smoothes" the ranking so that documents appearing consistently near the top across different searches are prioritized.
    *   **Formula**: $Score(d) = \sum_{r \in R} \frac{1}{k + rank(r, d)}$
*   **Example**: If Document A is ranked **1st** by a vector search and **3rd** by a keyword search (with $k=60$), its score is $\frac{1}{60+1} + \frac{1}{60+3} = 0.0164 + 0.0158 = 0.0322$.

*   #### 📊 Example

   * Retriever A: Doc1, Doc2, Doc3
   * Retriever B: Doc3, Doc2, Doc4
   
   * RRF scores:
      - Doc2 → appears high in both → high score  
      - Doc3 → appears in both → strong  
      - Doc1 → only in A → lower  
      - Doc4 → only in B → lower  

   * 👉 Final ranking:
      - Doc2 > Doc3 > Doc1 ≈ Doc4

#### 🧠 Usage
- Hybrid search (BM25 + embeddings)
- Production-grade RAG systems (very common)
- When scores are not comparable across models

---

### 2. Weighted Sum (Linear Fusion)
**Definition**: This method combines the raw similarity scores from different retrievers by assigning a weight (importance) to each source and summing them.

*   **Explanation**: It requires normalizing scores from different retrievers (e.g., between 0 and 1) because vector scores (cosine similarity) and keyword scores (BM25) use entirely different scales.
*   **Example**: You might decide that semantic search is twice as important as keyword search.
    *   **Calculation**: $(0.7 \times \text{Vector Score}) + (0.3 \times \text{Keyword Score})$.

* ### 📊 Example

   * BM25 score: Doc1: 0.8, Doc2: 0.6
   * Embedding score: Doc1: 0.5, Doc2: 0.9
   * Weights: BM25 = 0.6, Embedding = 0.4
   * Final: Doc1 = 0.60.8 + 0.40.5 = 0.68 , Doc2 = 0.60.6 + 0.40.9 = 0.72
   * 👉 Doc2 wins
---

### 3. Distribution-Based Score Fusion (DBSF)
**Definition**: DBSF is a specialized score-based fusion that normalizes results by accounting for the specific statistical distribution of scores within each retriever's result set.

*   **Explanation**: Standard normalization (like Min-Max) can be skewed by outliers. DBSF analyzes the mean and variance of the scores in each list to ensure that one retriever's "high" score truly represents high confidence relative to its own typical output before merging it with others.
*   **Example**: If Retriever A typically returns scores between 0.1 and 0.2, and Retriever B returns 0.8 to 0.9, DBSF adjusts these ranges so a "0.2" from A is treated with equal significance to a "0.9" from B.

* 💡 **Intuition**  
Different retrievers produce scores on different scales:

- **BM25** → wide range  
- **Embeddings** → cosine similarity (-1 to 1)

👉 DBSF converts them into a common distribution space.

📌 **Typical Process**

1. Compute mean & std of scores per retriever  
2. Normalize (z-score):

   $$
   z = \frac{x - \mu}{\sigma}
   $$

3. Combine (sum or weighted sum)

📊 **Example**

   * Retriever A scores: [10, 8, 5]
   * Retriever B scores: [0.9, 0.7, 0.6]
   * After normalization:
      * A → [1.2, 0.5, -0.8]
      * B → [1.0, 0.2, -0.5]
   * Now combine → comparable!

🧠 Usage

When score scales differ significantly
More principled than naive weighted sum
Useful in multi-retriever systems


---

### 4. Alpha Weighting ($\alpha$-weighting)
**Definition**: This is a specific parameter-driven version of hybrid fusion where a single value, **Alpha ($\alpha$)**, controls the balance between two different retrieval methods.

*   **Explanation**: It is a simplified weighted sum where $\alpha$ represents the weight of the first retriever (usually Vector) and $(1 - \alpha)$ represents the weight of the second (usually BM25).
*   **Example**: Setting $\alpha = 1.0$ makes the system purely semantic (vector-only), while $\alpha = 0.5$ creates an equal 50/50 split between keyword and semantic results.

### Summary Comparison Table


| Method | Type | Primary Signal | Key Advantage |
| :--- | :--- | :--- | :--- |
| **RRF** | Rank-based | Position in list | No score normalization needed; robust. |
| **Weighted Sum**| Score-based | Raw similarity | Allows precise tuning of retriever importance. |
| **DBSF** | Score-based | Statistical distribution | More accurate when score scales vary wildly. |
| **Alpha** | Score-based | Parametric weight | Easy to tune via a single "slider" value. |
