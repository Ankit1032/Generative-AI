# GraphRAG Relationship Creation

In a typical GraphRAG system, relationships are primarily created **automatically using an LLM**, though some specialized variants use traditional **Natural Language Processing (NLP)** techniques to reduce costs.

### How Relationships are Created
The creation process generally follows these steps:

*   **LLM Extraction (Standard)**: The system prompts an LLM to read through document segments (text units) to identify pairs of entities and describe how they are related. For example, given the sentence "Elon Musk founded SpaceX," the LLM extracts the relationship "founded" between the source entity "Elon Musk" and target entity "SpaceX".
*   **NLP Co-occurrence (Fast Variant)**: In "FastGraphRAG" methods, relationships are often defined more simply as the **co-occurrence** of two entities within the same text unit. This avoids expensive LLM calls but doesn't provide a detailed description of *why* they are related.
*   **Refinement & Summarization**: Once raw relationships are extracted, an LLM is often used again to **deduplicate** and **summarize** multiple instances of the same relationship found across different documents into a single, concise description.
*   **Relationship Weighting**: The LLM or the system assigns a **weight** or strength score to the relationship based on frequency and semantic importance.

### Can they be created manually?
While the core value of GraphRAG is **automated extraction** at scale, manual intervention is possible and sometimes necessary:

*   **Prompt Tuning**: Developers often **manually tune the extraction prompts** to define what kinds of relationships are relevant to their specific domain (e.g., "lives in" for news vs. "catalyzes" for chemistry).
*   **Custom Schemas**: Users can manually define a strict schema or ontology (e.g., using Pydantic) to force the LLM to only extract specific types of relationships.
*   **Manual Refinement**: After the initial graph is built, human users can audit and refine the LLM-generated nodes and edges to ensure accuracy.
