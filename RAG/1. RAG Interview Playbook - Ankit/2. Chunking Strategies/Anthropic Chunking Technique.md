# Anthropic's Contextual Retrieval (Contextual Embeddings)

Anthropic's chunking technique, known as Contextual Retrieval (or Contextual Embeddings), is a method designed to improve Retrieval-Augmented Generation (RAG) systems by addressing the loss of context that occurs when breaking down large documents into smaller, independent chunks. 

Instead of just splitting text and embedding it, this technique uses a large language model (like Claude) to add specific, concise context to each individual chunk before it is embedded and stored in a vector database.

---

## How Contextual Retrieval Works

### Traditional Chunking (The Problem)
- A large document is split into smaller segments (chunks).
- If a chunk says, "The revenue grew by 3%," the AI lacks context (company name, year) to understand it, leading to poor search results.

### Contextual Generation (The Solution)
- Anthropic prompts Claude to generate a short, specific summary for each chunk that captures the context of the surrounding text.

### Contextual Injection
- This context is prepended to the original chunk.

**Example:**
- "This is a financial report for ACME Corp in Q2 2023..." + "The company's revenue grew by 3%..."

### Embedding and Indexing
- The enriched chunk is converted into an embedding, capturing the nuanced meaning.

### Efficient Processing
- To keep costs low, Anthropic uses prompt caching, as the overall document context remains constant while processing multiple chunks.

---

## Key Benefits

### Significantly Higher Retrieval Accuracy
- Anthropic found that this method reduces top-20 retrieval failures by 35% on its own, and by up to 49% when combined with Contextual BM25 (a keyword-based search technique).

### Better Context Preservation
- It prevents the loss of meaning that often happens with traditional "naïve" chunking methods.

### Reduced RAG Hallucinations
- Because the retrieval is more accurate, the generative AI model receives better context, resulting in more reliable answers.

---

## Implementation Details

- Gemini or Voyage embeddings, and Claude 3.5 Sonnet can be used to generate the context.
- Reranking models can be used to refine the top-k retrieved chunks, which can boost performance by up to 67%.
- Prompt caching makes this process economical even for large knowledge bases.

---

## Links

1. Introducing Contextual Retrieval (Anthropic) : https://www.anthropic.com/engineering/contextual-retrieval  
2. The best RAG’s technique yet? Anthropic’s Contextual Retrieval and Hybrid Search : https://www.linkedin.com/pulse/best-rags-technique-yet-anthropics-contextual-hybrid-search-siddiqui-934zc/
