# Types of Chunking Strategies

## Fixed-size Chunking (Naive)
- Splits text into chunks of a set number of tokens or characters, often with a fixed overlap to prevent losing context between boundaries.

## Recursive Character Chunking
- A sophisticated, hierarchical approach that attempts to split text using a set of separators (e.g., paragraphs, newlines, spaces) to keep related text together while maintaining a target size.

## Semantic Chunking
- Analyzes the semantic meaning of sentences, splitting only when semantic similarity drops below a threshold.
- This ensures coherent, context-rich chunks, though it is more computationally intensive.

## Content-Aware / Document-Based Chunking
- Leverages structure (e.g., Markdown headers, HTML tags, or document layout) to make logical splits.

## Agentic / LLM-Based Chunking
- Uses an LLM to evaluate the text and determine the most logical points to split, offering the highest quality but lowest speed.

---

## Key Considerations

### Chunk Size
- Smaller chunks (128–256 tokens) are best for precise queries, while larger chunks (512+ tokens) suit summaries.

### Overlap
- 10–20% overlap between chunks is standard to maintain continuity.

### Evaluation
- Experiment with different sizes and methods (e.g., using Pinecone or LangChain) to find the best strategy for your data.
