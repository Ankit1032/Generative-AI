# SPLADE: SParse Lexical AnD Expansion

**SPLADE** is a neural retrieval model that creates "smart" sparse vectors for text. It bridges the gap between traditional keyword search (like BM25) and modern semantic search by using deep learning to understand context while keeping the output in an interpretable keyword-like format.

---

## How it Works

Unlike traditional models that only count words present in a text, SPLADE uses a **Transformer-based model** (usually BERT) to predict the importance of every word in its entire vocabulary for a given piece of text.

The process generally follows these steps:

1. **Contextual Encoding**: The text is passed through a transformer. The model looks at how words relate to each other in the sentence rather than treating them as isolated terms.
2. **Term Weighting**: The model assigns a weight to each token. Important keywords get high scores, while "filler" words like "the" or "and" are pushed toward zero.
3. **Term Expansion**: This is SPLADE's "killer feature." It can activate and assign weights to terms that **do not appear** in the original text but are semantically related. 
    * *Example*: A query for "lunar" might automatically have "moon" added to its vector with a high weight.
4. **Sparsification**: To keep the vector efficient, a mathematical "mask" (regularization) is applied so that only the most relevant ~100–300 terms (out of a 30,000+ vocabulary) have non-zero values.

---

## Key Benefits

* **Fixes Vocabulary Mismatch**: It finds relevant documents even if the user uses different words than the author (e.g., searching for "jungle" and finding documents about a "rainforest").
* **Interpretability**: Since each dimension in the vector corresponds to a real word, you can inspect the vector and see exactly why a document was retrieved.
* **Infrastructure Compatibility**: Because the output is a sparse vector, it can often be used with existing search engines like **Elasticsearch** or **Solr** that already use inverted indexes.
* **Hybrid Search**: It is frequently used alongside dense vectors in databases like **Qdrant**, **Pinecone**, or **Milvus** to combine exact keyword matching with deep semantic understanding.

---

## Comparison At a Glance


| Feature | Traditional (BM25) | Dense Vectors (BERT) | SPLADE |
| :--- | :--- | :--- | :--- |
| **Matching** | Exact Keywords only | Purely Semantic | Keywords + Contextual |
| **Expansion** | None (unless manual) | Implicit | **Automatic & Transparent** |
| **Interpretability** | High | Low (Black box) | **High** |
