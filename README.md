
# Document Summarization using RAG, LangChain, LangGraph

## Features
- PDF Upload
- RAG Pipeline
- LangGraph Workflow
- FAISS Vector Store
- OpenRouter + Llama 3.1 8B Instruct
- Multiple Summary Lengths
- Retrieved Context Display
- Download Summary
- Metrics Dashboard
- Model Selection Methodology (ROUGE, BERTScore, Latency)

## Architecture
PDF -> Loader -> Chunking -> Embeddings -> FAISS -> Retriever -> LangGraph -> Llama -> Summary

## Run
pip install -r requirements.txt
streamlit run app.py
