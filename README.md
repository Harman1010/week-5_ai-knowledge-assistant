Welcome to AI Knowledge Assistant

This project is about using production RAG to retrieve relevant context and query over company documents.
This is a step ahead of standard RAG as it extends that pipeline by adding more features that enhances the quality of 
RAG pipeline.

This also includes evaluation as well so we'll verify the choices we make.

---

## Features

- Hybrid Search
- Guardrails
- Prompt evaluation
- Single Responsibility Principle
- Reranking

---

## Tech Stack

### Frontend

- Gradio

### Backend

- FastAPI

### AI

- LangChain
- SentenceTransformers
- CrossEncoder
- BM25 + Semantic similarity
- Guardrails
- RAGAS

---

## Architecture

```text
                         Company PDF
                              |
                              v
                    Document Ingestion
                              |
                              v
                         Chunking
                              |
                              v
                       Query / Documents
                              |
              +---------------+---------------+
              |                               |
              v                               v
        Semantic Search                  BM25 Search
            (FAISS)                     (Keyword)
              |                               |
              +---------------+---------------+
                              |
                              v
                    Reciprocal Rank Fusion
                              |
                              v
                     Candidate Documents
                              |
                              v
                     Cross-Encoder Reranker
                              |
                              v
                       Top-K Context
                              |
                              v
                         Gemini LLM
                              |
                              v
                    Structured Response
                              |
                +-------------+-------------+
                |                           |
                v                           v
              Answer                    Sources

```

---

### Project Structure

AI-Knowledge-Assistant/
│
├── backend/
│   ├── __init__.py
│   └── app.py
│
├── frontend/
│   └── ...
│
├── rag/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── hybridSearch.py
│   ├── query_transform.py
│   └── retrieval.py
│
├── routes/
│   ├── __init__.py
│   ├── ask.py
│   └── upload.py
│
├── schemas/
│   ├── __init__.py
│   ├── request.py
│   └── response.py
│
├── services/
│   ├── __init__.py
│   ├── bm25.py
│   ├── embeddings.py
│   ├── generation_service.py
│   ├── knowledgeService.py
│   ├── llm_service.py
│   ├── rerank.py
│   └── vectorService.py
│
├── evaluation/
│   └── ...
│
├── utils/
│   ├── __init__.py
│   └── config.py
│
├── test_ingestion.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

---

## Setup Guide

### 1. Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Knowledge-Assistant

```

### 2. Initiate virtual environment

```powershell

python -m venv venv

```

### 3. Activate virtual environment

```powershell

venv\Scripts\activate.ps1

```

### 4. Install dependencies

```powershell

pip install -r requirements.txt

```
### 5. Setup API Key

Refer to .env.example

### 6. Start the FastAPI server

```powershell

uvicorn backend.app:app

```

---


---

### Limitations

- The current system primarily supports PDF-based company documents.
- FAISS indexes are currently maintained in memory and are not persisted between application restarts.
- BM25 currently uses basic tokenization and may not handle complex linguistic variations optimally.
- Query transformation requires an additional LLM call, which can increase latency and API usage.
- Cross-Encoder reranking provides better relevance scoring but is more computationally expensive than standard vector retrieval.
- The quality of the final answer depends on the quality of the retrieved context.

---

### Future Improvements

- Add persistent vector database storage instead of maintaining FAISS indexes only in memory.
- Implement advanced input, retrieval, and output guardrails.
- Add document-level access control and role-based permissions.
- Implement grounding verification and hallucination detection.
- Integrate automated RAG evaluation using RAGAS.
- Build a larger evaluation dataset containing real enterprise-style queries.

---
