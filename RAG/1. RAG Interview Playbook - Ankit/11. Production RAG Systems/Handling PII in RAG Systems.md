# Handling PII in RAG Systems

Handling Personally Identifiable Information (PII) in a Retrieval-Augmented Generation (RAG) system requires a **multi-layered approach** to ensure that sensitive data is neither stored in plain text nor leaked to external LLM providers.

## 1. Pre-Processing: Redaction at Ingestion

The most secure practice is to detect and redact PII **before** it ever reaches your vector database or embedding model.

- **Identify PII**: Use tools like Microsoft Presidio (Python-based), spaCy, or cloud services like Amazon Comprehend to detect names, emails, phone numbers, and IDs.
- **Masking vs. Redacting**: Instead of just stripping text (which can destroy context), replace PII with typed surrogate tokens (e.g., `[PERSON_1]`, `[EMAIL_2]`).
- **Reversible Mapping**: Store the original values and their corresponding tokens in a separate, highly secure, and access-controlled database (like Firestore or a private SQL instance). This allows you to re-insert the real data into the final response for authorized users only.

## 2. Retrieval Hygiene

Even if your database is redacted, the query and retrieval stages need safeguards:

- **Query Redaction**: Run the same PII detection on the user's input query before it is sent for embedding or retrieval.
- **Similarity Search Risks**: Ensure the vector DB does not unintentionally return high-confidence matches for sensitive patterns. Use hybrid search (combining keyword and vector search) to improve recall when searching for specific surrogate IDs.
- **Role-Based Access (RBAC)**: Implement metadata filtering in your vector store so users only retrieve document chunks they have permission to see.

## 3. Generation and Egress: The "Belt-and-Suspenders"

The final stage prevents "accidental echoes" of PII in the LLM's response.

- **Output Scrubbing**: Scan the LLM’s final response for PII-like strings (e.g., credit card formats or API keys) before displaying it to the user.
- **De-anonymization**: If the user is authorized, replace the surrogate tokens in the LLM's response with the original values from your secure mapping store.
- **Strict Prompting**: Use system prompts that explicitly instruct the model to only use provided context and avoid generating or hallucinating personal details.

## Recommended Tools

- **LlamaIndex PII Postprocessors**: Built-in nodes for masking PII using NER models or local LLMs before data is sent to external APIs.
- **Microsoft Presidio**: Highly extensible and customizable for specific PII types (e.g., IBAN, medical licenses).
- **Amazon Bedrock Guardrails**: Provides inference-time filtering to block sensitive information from LLM inputs and outputs.
