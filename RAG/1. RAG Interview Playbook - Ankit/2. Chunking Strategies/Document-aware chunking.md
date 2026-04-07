# Document-aware chunking

Document-aware chunking improves RAG by splitting text based on structure (headings, paragraphs) rather than fixed character counts. Using Python and LangChain, you can implement this by identifying structural markers (e.g., #, ##) to ensure chunks maintain semantic context. Key methods include MarkdownTextSplitter and RecursiveCharacterTextSplitter.

---

## 1. Markdown-Aware Chunking (Best for MD/Docs)

If your documents are in Markdown format, use LangChain's MarkdownTextSplitter to split based on header levels, which keeps sections together.

```python
from langchain.text_splitter import MarkdownTextSplitter
from langchain.schema import Document

# Sample Markdown document
markdown_text = """
# Company Policy
## Introduction
This is the introduction section.
## Remote Work Policy
Employees can work from home.
## Holidays
Public holidays are observed.
"""

# Initialize the splitter
splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=0)

# Create documents
chunks = splitter.create_documents([markdown_text])

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk.page_content}\n")
```

---

## 2. Recursive Structure Chunking (Best for Unstructured Text)

For general text, use RecursiveCharacterTextSplitter. It splits by paragraphs (\n\n), then sentences (.), preserving semantic structure.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create the splitter with specific separators
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)

with open("company_report.txt") as f:
    sample_text = f.read()

# Split text
docs = splitter.create_documents([sample_text])
print(f"Created {len(docs)} chunks")
```

---

## 3. Adding Metadata to Chunks

To make chunks truly document-aware, add metadata, such as the document title or section header, to each chunk. This ensures the retriever knows which part of the document the chunk belongs to.

```python
from langchain.schema import Document

def create_aware_chunks(text, title):
    # Perform initial split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    chunks = text_splitter.split_text(text)
    
    # Wrap in Document object and add metadata
    return [
        Document(page_content=chunk, metadata={"source": title, "chunk_id": i})
        for i, chunk in enumerate(chunks)
    ]

# Usage
doc_chunks = create_aware_chunks("Very long document text...", "Q1 Report")
```

---

## Links

1. Optimal way to chunk word document for RAG(semantic chunking giving bad results): https://community.openai.com/t/optimal-way-to-chunk-word-document-for-rag-semantic-chunking-giving-bad-results/687396  
2. The Ultimate Guide to Chunking Strategies for RAG Applications with Databricks: https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089#:~:text=%23%20Create%20the%20text%20splitter%20with,%7Bexample_chunk.metadata%7D%22)  
3. Layout-Aware-Document-Extraction-Chunking-and-Indexing: https://github.com/aws-samples/layout-aware-document-processing-and-retrieval-augmented-generation
