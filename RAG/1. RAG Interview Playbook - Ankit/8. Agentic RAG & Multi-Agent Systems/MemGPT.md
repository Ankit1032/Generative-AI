# MemGPT

**MemGPT** (Memory-GPT) is a system designed to give Large Language Models (LLMs) virtually unlimited memory by managing information like a computer operating system.

Developed by researchers at **UC Berkeley**, it addresses a major limitation of models like GPT-4: the "context window," or the maximum amount of text they can process at once. When a conversation gets too long, standard LLMs "forget" the beginning; MemGPT solves this by moving information in and out of the active window as needed.

### How It Works
MemGPT treats the LLM like a processor and uses a tiered memory system:

*   **Main Context (RAM):** The model's immediate "working memory." This is the standard, limited window where the AI currently "thinks".
*   **External Context (Disk Storage):** A massive, searchable archive where MemGPT stores data that doesn't fit in the main context.
    *   **Recall Storage:** Stores the entire history of past conversations.
    *   **Archival Storage:** A general database for large documents or facts.
*   **Self-Management:** The LLM itself decides when to "page" information between these tiers using function calls. If it needs a fact from three months ago, it searches its external storage and brings it back into the main context.

### Key Benefits
*   **Persistent Personalities:** Unlike standard bots that reset every session, MemGPT agents can remember your preferences and past interactions over months or years.
*   **Deep Document Analysis:** It can "read" and analyze massive documents (like legal contracts or research papers) that are far too large for a standard model's context window.
*   **Consistency:** By managing its own memory, it avoids "context pollution"—getting confused by too much irrelevant information—and maintains more coherent long-term dialogues.

MemGPT is available as an [open-source Python package](https://github.com) that can be integrated with various LLMs, including OpenAI's models and local models like Llama.
