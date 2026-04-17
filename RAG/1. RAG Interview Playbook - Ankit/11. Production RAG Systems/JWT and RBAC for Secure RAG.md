# JWT and RBAC for Secure RAG

In a Retrieval-Augmented Generation (RAG) system, **JWT (JSON Web Tokens)** and **RBAC (Role-Based Access Control)** work together to ensure that sensitive documents are only retrieved and used by authorized users. This prevents **"data leakage"** where an AI might inadvertently reveal confidential information to a user who doesn't have the right permissions.

## The Role of JWT

JWT is the secure vehicle used to carry a user's identity and permissions across the system without needing a central session database.

- **Identity Transmission**: When a user logs in, they receive a signed JWT containing **"claims"**, such as their `user_id` and assigned role.
- **Stateless Authentication**: Every request the user makes to the RAG backend includes this token. The backend verifies the token's signature to ensure it hasn't been tampered with.
- **Role Delivery**: The role inside the JWT (e.g., "Engineering" or "Sales") is extracted by the RAG application to determine which documents the user can "see" during the retrieval phase.

## The Role of RBAC

RBAC is the logic layer that dictates what each role is allowed to do.

- **Metadata Filtering**: In a RAG pipeline, documents in the vector database are tagged with metadata specifying which roles have access (e.g., `access_role: ["admin", "hr"]`).
- **Constrained Retrieval**: When a user asks a question, the system uses the role from their JWT to filter the search. Only documents matching the user's role are retrieved as context for the LLM.
- **Granular Access**: Organizations can define specific boundaries, such as an HR employee only getting answers based on leave policies while finance staff only see expense data.

## How They Work Together in a RAG Pipeline

1. **Authentication**: The user logs in and receives a JWT containing their role.
2. **Query & Token Pass**: The user sends a query (e.g., "What is our Q3 revenue?") along with their JWT.
3. **RBAC Enforcement**: The system extracts the role from the JWT and applies a metadata filter to the vector search (e.g., `role == 'finance'`).
4. **Secure Generation**: The LLM receives only the authorized context to generate a response, ensuring no unauthorized data is leaked.
