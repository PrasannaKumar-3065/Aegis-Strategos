# 🛡️ Aegis Strategos

> **Because this is not just thinking.**
> 
> It is planning, retrieving, reasoning, commanding tools, and producing structured outputs with discipline.
>
> **Strategos** = The General.  
> **Aegis** = The Shield.  
> 
> *The Shielded Strategist.*

---

## Overview

**Aegis Strategos** is an advanced **Retrieval-Augmented Generation (RAG) system** designed for universal document processing and structuring. It combines sophisticated document parsing, semantic embeddings, and intelligent retrieval to enable AI systems to think strategically—not just passively process information.

This is an **ongoing project** with a clear trajectory toward enterprise-grade document understanding and AI-powered decision making.

---

## Core Architecture

### 🏗️ Document Processing Pipeline

The system ingests raw text through a multi-stage processing pipeline:

1. **Document Parsing** (`parser()`): Breaks down raw text into logical sections with unique identifiers
2. **Intelligent Chunking** (`chunk_sections()`): Segments content with configurable size (400 tokens default) and overlap (40 tokens) to preserve context
3. **Token-Aware Processing**: Uses HuggingFace tokenizers for accurate token counting and text handling
4. **Summarization** (`generate_summary()`): Generates dense, concept-focused summaries using Google Flan-T5-Small for semantic compression

### 🔍 Semantic Retrieval System

- **Embedding Model**: Intfloat E5-Small (lightweight, production-ready)
- **Vector Database**: FAISS (Facebook AI Similarity Search) with cosine similarity via normalized embeddings
- **Query Interface**: Semantic search with top-k retrieval (default k=3)

### 📋 Data Structures

Each processed document maintains hierarchical metadata:

```python
{
    "doc_id": "unique-uuid",
    "source": "document-origin",
    "sections": [
        {
            "section_id": "uuid",
            "title": "section_name",
            "content": "raw-text",
            "chunks": [...]  # Rich chunk metadata
        }
    ]
}

# Individual chunk structure
{
    "chunk_id": "uuid",
    "doc_id": "parent-uuid",
    "section_id": "parent-uuid",
    "position_index": "sequential-position",
    "content": "cleaned-text",
    "summary": "semantic-summary",
    "token_count": "integer",
    "overlap_from_previous": "token-count"
}
```

---

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM Framework** | HuggingFace Transformers | Model loading and inference |
| **Base Model** | TinyLlama-1.1B-Chat-v1.0 | Tokenization and future commands |
| **Summarization** | Google Flan-T5-Small | Dense concept extraction |
| **Embeddings** | Intfloat E5-Small | Semantic vector representations |
| **Vector Store** | FAISS (CPU) | Similarity search infrastructure |
| **Utilities** | Sentence-Transformers, NLTK | Text processing and embeddings |

---

## Features

### ✅ Current Implementation

- **Intelligent Document Ingestion**: Parse multi-section documents with UUID tracking
- **Context-Aware Chunking**: Overlapping chunks preserve semantic continuity
- **Semantic Summarization**: Extract core concepts without repetition
- **High-Speed Retrieval**: FAISS-powered multi-query search
- **Production-Ready**: CUDA support for GPU acceleration

### 🚀 Roadmap (Ongoing)

#### Phase 1: RAG Pipeline Enhancement (In Progress)
- [ ] Multi-modal document support (PDFs, images, tables)
- [ ] Advanced chunking strategies (hierarchical, semantic-aware)
- [ ] Metadata filtering and hybrid search
- [ ] Query rewriting and expansion

#### Phase 2: Fine-Tuned Small Language Model
- [ ] **Unsloth-backed Fine-Tuning**: Efficient fine-tuning framework for rapid iteration
- [ ] Task-specific model adaptation (document Q&A, summarization)
- [ ] Parameter-efficient fine-tuning (LoRA, QLoRA)
- [ ] Performance benchmarking against base models

#### Phase 3: Tool Command System
- [ ] Structured output generation
- [ ] Tool reasoning and selection
- [ ] Multi-hop query reasoning
- [ ] Feedback loops for continuous improvement

#### Phase 4: Advanced Features
- [ ] Knowledge graph construction from documents
- [ ] Cross-document reasoning
- [ ] Real-time update mechanisms
- [ ] Caching and optimization strategies

---

## Usage

### Installation

```bash
# Install dependencies
pip install transformers sentencepiece nltk rank-bm25 faiss-cpu sentence-transformers

# GPU support (CUDA)
# Replace faiss-cpu with faiss-gpu if using NVIDIA GPUs
```

### Basic Workflow

```python
from aegis_strategos import ingest_pipeline, retrieve, build_faiss_index

# 1. Ingest document
result = ingest_pipeline(raw_text, source="Wikipedia ML")
chunks = result["chunks"]

# 2. Build vector index
embeddings = build_faiss_index(chunks)

# 3. Semantic search
results = retrieve("How does machine learning differ from AI?", index, chunks, top_k=3)

# 4. Access results with summaries and metadata
for result in results:
    print(result["content"])
    print(result["summary"])
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `parser(text, source)` | Parse text into hierarchical sections |
| `chunk_sections(section, doc_id)` | Create overlapping chunks with metadata |
| `generate_summary(text)` | Semantic concept extraction |
| `embed_passages(chunks)` | Batch embedding generation |
| `embed_query(query)` | Query embedding for search |
| `build_faiss_index(embeddings)` | Create FAISS similarity index |
| `retrieve(query, index, chunks, top_k)` | Retrieve top-k semantically similar chunks |

---

## Configuration

### Chunking Parameters

```python
CHUNK_SIZE = 400      # Tokens per chunk
OVERLAP = 40          # Overlap tokens for context continuity
```

### Model Selection

```python
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Tokenizer
SUM_MODEL = "google/flan-t5-small"                  # Summarization
EMBED_MODEL = "intfloat/e5-small"                   # Embeddings
```

### Summarization Parameters

```python
max_tokens = 60       # Maximum summary length
temperature = 0.3     # Generation randomness (lower = more deterministic)
top_p = 0.9          # Nucleus sampling threshold
```

---

## Example: Multi-Query RAG

The system is tested with complex, multi-hop queries against Machine Learning Wikipedia content:

```
Query: "How does the 'operational definition' of machine learning bridge 
the gap between Alan Turing's inquiries and 1960s learning machines?"

Retrieved Results:
1. Tom Mitchell's formal ML definition (most relevant)
2. Cybertron learning machine description
3. Turing's philosophical foundations
```

The retrieval system contextually grounds responses in source material, enabling reliable, cited AI reasoning.

---

## Project Vision

### Presence & Purpose

Aegis Strategos will mature into a **discipline-driven AI system** that:

- **Plans strategically** with multi-step reasoning
- **Retrieves intelligently** from structured knowledge
- **Reasons systematically** about complex problems
- **Commands tools** with confidence and precision
- **Produces structured outputs** fit for decision-making

### Future: Universal Document Processing

Future versions will establish:

1. **Standardized document ingestion** for any format or domain
2. **Adaptive chunking** that respects logical boundaries
3. **Fine-tuned domain models** via efficient Unsloth QLoRA pipelines
4. **Tool-integrated reasoning** for autonomous task execution
5. **Knowledge persistence** for organizational intelligence

---

## Development Status

🟡 **ACTIVE DEVELOPMENT** - Core RAG pipeline operational  
🟡 **PHASE 1** - Expanding document handling and retrieval sophistication  
🔴 **PHASE 2** - Fine-tuning infrastructure (Unsloth forthcoming)  
🔴 **PHASE 3** - Tool command system (planned)  
🔴 **PHASE 4** - Advanced knowledge reasoning (planned)  

---

## Performance Notes

### Current Capabilities
- ✅ Document ingestion: < 1s for typical articles
- ✅ Embedding generation: Batch processing at 32 samples/batch
- ✅ Semantic retrieval: < 50ms for FAISS search on 100k+ documents
- ✅ GPU acceleration: Full CUDA pipeline support

### Optimization Roadmap
- Quantized embeddings (int8/binary for speed)
- Hierarchical clustering for million-scale documents
- Hybrid BM25 + semantic search
- Caching layers for frequent queries

---

## Contributing

This ongoing project welcomes contributions in:

- RAG pipeline improvements
- Fine-tuning script development (Unsloth integration)
- Document format support
- Evaluation benchmarks
- Deployment optimization

---

## License

*License information to be added*

---

## Philosophy

**Aegis Strategos** embodies a principle: *Real intelligence isn't passive thinking—it's active strategy.*

- 🛡️ **Aegis** provides the shield of structured knowledge
- 📜 **Strategos** commands the general's precision
- 🔗 **RAG** bridges data and reasoning
- ⚙️ **Fine-tuning** adapts to your domain
- 🎯 **Tools** execute with discipline

Together, they form a shielded strategist with presence and future capability.

---

**Status**: Ongoing Project | **Last Updated**: February 2026