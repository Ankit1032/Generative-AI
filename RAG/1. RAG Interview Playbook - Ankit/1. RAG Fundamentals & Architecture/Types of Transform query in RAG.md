# Query Transformation in RAG

Query transformation is a critical component of advanced Retrieval-Augmented Generation (RAG) systems that modifies, refines, or decomposes a user's initial prompt to improve retrieval accuracy and the quality of the generated answer.

It bridges the gap between how users talk and how data is stored.

---

## Primary Types & Techniques

### 1. Query Rewriting (Refinement)
**What it does:**
- Rewrites the query to remove ambiguity
- Improves semantic understanding before retrieval

**Use Case:**
- Vague, incomplete, or poorly phrased queries

**Example:**
- "What's the deadline for leaving?"  
  → "Resignation notice period policy"

---

### 2. Query Expansion (Augmentation)
**What it does:**
- Adds synonyms, related terms, or contextual keywords
- Broadens search scope

**Use Case:**
- When user terminology differs from document vocabulary
- Improves recall

---

### 3. Sub-query Decomposition (Decomposition)
**What it does:**
- Breaks complex queries into smaller sub-queries
- Each sub-query is answered individually

**Use Case:**
- Multi-hop reasoning
- Complex research questions

**Example:**
- "How does company A's revenue compare to B?"  
  → "What is company A's revenue?"  
  → "What is company B's revenue?"

---

### 4. Hypothetical Document Embeddings (HyDE)
**What it does:**
- Generates a hypothetical answer using an LLM
- Converts it into an embedding
- Uses it to retrieve similar real documents

**Use Case:**
- Short, vague, or highly technical queries
- When query doesn't align with document semantic space

---

### 5. Multi-Query Rewriting (Fanout)
**What it does:**
- Generates multiple variations of the query
- Executes them in parallel
- Merges results (e.g., Reciprocal Rank Fusion)

**Use Case:**
- Complex or open-ended queries
- When a single interpretation is insufficient

---

### 6. Step-back Prompting
**What it does:**
- Converts query into a more general/abstract form
- Retrieves foundational concepts first

**Use Case:**
- When query is too specific and retrieval fails

**Example:**
- "Why does my Tesla battery die fast in cold?"  
  → "How does temperature affect electric vehicle batteries?"

---

### 7. Corrective RAG (CRAG)
**What it does:**
- Evaluates retrieved documents
- If low quality → triggers new retrieval (e.g., web search)

**Use Case:**
- High-stakes domains (legal, medical)
- When reliability is critical

---

## Summary of Query Transformation Techniques

| Type         | Goal                  | Best For                          |
|--------------|-----------------------|-----------------------------------|
| Rewriting    | Clarity & Context     | Vague, ambiguous queries          |
| Expansion    | Better Recall         | Technical jargon, acronyms        |
| Decomposition| Multi-hop reasoning   | Complex, multi-part questions     |
| HyDE         | Semantic Matching     | Vague queries (finding answers)   |
| Fanout       | Comprehensive Search  | Complex, open-ended queries       |
| Step-back    | Conceptual Retrieval  | High-level, abstract questions    |
| Corrective   | Verification          | High-accuracy requirements        |
