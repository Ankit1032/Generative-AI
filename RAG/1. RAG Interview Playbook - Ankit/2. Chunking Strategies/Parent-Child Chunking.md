# Parent-Child Chunking

Parent-Child Chunking improves RAG by indexing small, specific child chunks for precise search while retrieving larger, context-rich parent chunks for the LLM. You create parent chunks (e.g., 1000 tokens), split them into child chunks (e.g., 200 tokens), store children in a vector store, and map children back to parents via IDs.

---

## Implementation Steps (LangChain)

- Define Splitters: Use a large splitter for parents and small for children.
- Initialize Storage: Use InMemoryStore or a vector DB to store parents.
- ParentDocumentRetriever: Combine them. 

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# 1. Splitters for Parent-Child
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# 2. VectorDB for child chunks (searching), Docstore for parent chunks (retrieval)
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
store = InMemoryStore() 

# 3. Initialize Retriever
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# Example Usage
docs = [Document(page_content="...Full document content...")]
retriever.add_documents(docs)

# Search
results = retriever.invoke("Query")
```

---

## Key Benefits

- Reduced Hallucinations: The LLM receives broader context.
- High Precision: Small embeddings find exact answers.
- Efficiency: Smaller embeddings mean faster similarity searches.

---

## Links

1. ParentDocumentRetriever : https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever  
2. The Beauty of Parent-Child Chunking. Graph RAG Was Too Slow for Production, So This Parent-Child RAG System was useful: https://www.reddit.com/r/Rag/comments/1mtcvs7/the_beauty_of_parentchild_chunking_graph_rag_was/#:~:text=Parent%20Chunks:%20I%20first%20split,documents%2C%20just%20the%20smaller%20children.  
3. Parent-Child Chunking in LangChain for Advanced RAG: https://medium.com/@seahorse.technologies.sl/parent-child-chunking-in-langchain-for-advanced-rag-e7c37171995a
