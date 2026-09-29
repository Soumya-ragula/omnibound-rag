# Omnibound RAG API

A production-oriented Retrieval-Augmented Generation (RAG) API built with FastAPI, Pinecone, embeddings, and Google Gemini.

## Architecture

Document
    ↓
FastAPI
    ↓
Document Loader
    ↓
Text Chunking
    ↓
Embeddings
    ↓
Pinecone Vector Database
    ↓
Semantic Retrieval
    ↓
Context
    ↓
Google Gemini
    ↓
Answer + Sources

## Features

- Multi-tenant document ingestion
- PDF and text document processing
- Text chunking
- Vector embeddings
- Pinecone vector storage
- Semantic document retrieval
- Google Gemini LLM integration
- Source metadata in query responses
- FastAPI REST API
- Swagger/OpenAPI documentation
- Docker containerization
- Automated API tests
- Gemini service fallback handling

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pinecone
- Google Gemini
- Docker
- Pytest
- Pydantic

## API Endpoints

### Health Check

```http
GET /