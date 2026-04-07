# Fine-Tuning an Embedding Model for Finance Corpus

Fine-tuning an embedding model for a finance corpus involves adapting a general-purpose model to recognize specialized terminology (e.g., "10-K filings," "EBITDA," or "indemnification") and complex semantic relationships unique to the industry. You can achieve significant improvements in retrieval accuracy (often **7–15%**) using relatively small datasets.

### 1. Prepare Your Finance Dataset
The quality of your dataset is the most critical factor.
*   **Data Formats**:
    *   **Positive Pairs**: Pairs of related text like `(question, relevant_context)` or `(query, answer)`.
    *   **Triplets**: `(anchor, positive, negative)` where the anchor is semantically closer to the positive than the negative.
*   **Sample Size**: Start with **2,000 to 5,000 high-quality samples** for narrow finance tasks. For highly specialized terminology, aim for **10,000+** samples.
*   **Synthetic Data Generation**: If you lack labeled pairs, use an LLM to generate synthetic questions from your finance corpus (e.g., SEC filings).

### 2. Select a Base Model
Start with a lightweight, high-performing model from the [Massive Text Embedding Benchmark (MTEB)](https://huggingface.co).
*   **Recommended Models**: `BAAI/bge-base-en-v1.5` or `all-MiniLM-L6-v2` are popular choices that can be fine-tuned easily using the [Sentence Transformers library](https://multivax.com).

### 3. Choose a Loss Function
The loss function must match your data format:
*   **MultipleNegativesRankingLoss (MNRL)**: Best if you only have positive pairs. It treats other samples in a batch as "in-batch negatives," providing a strong training signal.
*   **MatryoshkaLoss**: Useful for creating "nested" embeddings that remain effective even when truncated to smaller dimensions, reducing storage costs by up to 6x.
*   **TripletLoss**: Best if you have explicit "hard negatives" (texts that look similar but are irrelevant).

### 4. Execute the Fine-Tuning
Using the [SentenceTransformersTrainer](https://huggingface.co) simplifies the process:
*   **Epochs**: 1–2 epochs are usually sufficient for real-world data to avoid overfitting.
*   **Batch Size**: Use the largest batch size your GPU allows (e.g., 32, 64, or 128) because larger batches provide more in-batch negatives for MNRL.
*   **Learning Rate**: Start with a small rate like **2e-5** or **1e-5** with a 10% warmup.

### 5. Evaluation Metrics
Evaluate your model on a held-out test set using retrieval-focused metrics:
*   **NDCG@10** (Normalized Discounted Cumulative Gain): Measures ranking quality.
*   **MRR** (Mean Reciprocal Rank): How quickly the first relevant result appears.
*   **Recall@K**: Whether the relevant document is captured in the top K results.
