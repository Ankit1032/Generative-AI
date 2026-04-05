# Chunking Strategies

## Fixed-Size Chunking
- Character-based splitting
- Token-based splitting
- Chunk size selection (256/512/1024 tokens)
- Overlap strategies
- Pros and cons

**INTERVIEW PRIORITY:** ● ● ● ● ○

---

## Semantic Chunking
- Embedding similarity breakpoints
- Percentile / std-dev thresholds
- Sentence transformers for boundary detection
- LangChain SemanticChunker

**INTERVIEW PRIORITY:** ● ● ● ● ●

---

## Recursive Splitting
- RecursiveCharacterTextSplitter
- Hierarchical separators (\n\n, \n, space)
- Preserving semantic units

**INTERVIEW PRIORITY:** ● ● ● ○ ○

---

## Document-Aware Chunking
- Markdown header splitting
- HTML section splitting
- Code-aware splitting
- Table-aware chunking
- PDF structure extraction

**INTERVIEW PRIORITY:** ● ● ● ○ ○

---

## Advanced Chunking
- Proposition-based chunking (Dense X Retrieval)
- Late chunking
- Contextual chunk headers
- Parent-child chunk relationships
- RAPTOR recursive chunking

**INTERVIEW PRIORITY:** ● ● ● ● ○

---

## Chunk Size Trade-offs
- Recall vs precision
- Context richness vs noise
- Embedding quality degradation at extremes
- Benchmark-driven chunk size selection

**INTERVIEW PRIORITY:** ● ● ● ● ●
