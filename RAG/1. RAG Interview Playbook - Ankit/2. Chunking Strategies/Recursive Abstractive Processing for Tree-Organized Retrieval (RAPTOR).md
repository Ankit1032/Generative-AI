# Recursive Abstractive Processing for Tree-Organized Retrieval (RAPTOR)

Recursive Abstractive Processing for Tree-Organized Retrieval (RAPTOR) is a RAG (Retrieval-Augmented Generation) framework that improves how LLMs understand long documents by organizing text into a hierarchical tree structure. It recursively clusters and summarizes text chunks, allowing the model to retrieve both high-level summaries and fine-grained details for more comprehensive answers

---

## Key Aspects of RAPTOR

### Hierarchical Structure
- Instead of just a flat list of text chunks, RAPTOR builds a tree with multiple layers.
- The lowest layer contains the original text, while higher layers contain summaries of the layer below, created using LLMs.

### Clustering Algorithm
- It uses Gaussian Mixture Models (GMM) or similar clustering techniques to group semantically similar text segments together, rather than just relying on their linear order in the text.

### Improved Retrieval
- During querying, RAPTOR enables traversing this tree, allowing it to retrieve information at various levels of abstraction, which significantly improves performance on complex, multi-hop question-answering tasks.

### Key Advantage
- It specifically addresses the limitation of standard RAG models that struggle to capture broad context or long-distance dependencies across large documents.
