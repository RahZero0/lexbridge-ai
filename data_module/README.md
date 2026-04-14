# Data Module

A modular data ingestion, storage, and retrieval pipeline for QA datasets. Designed to feed **Agentic RAG**, **knowledge graphs**, and **fast vector retrieval** systems.

## Data Sources

| Source | License | Size | Access |
|---|---|---|---|
| Stack Exchange Dump (Apr 2024) | CC BY-SA 4.0 | ~100 GB | archive.org |
| Wikipedia Dumps | CC BY-SA 4.0 + GFDL | ~22 GB | dumps.wikimedia.org |
| Wikidata | CC0 | ~100 GB | dumps.wikimedia.org |
| SQuAD 2.0 | CC BY-SA 4.0 | ~50 MB | Hugging Face |
| Natural Questions | CC BY-SA 3.0 | ~4 GB | Google Cloud Storage |
| MS MARCO | CC BY 4.0 | ~2 GB | msmarco.org / HF |
| HotpotQA | CC BY-SA 4.0 | ~600 MB | hotpotqa.github.io |
| TriviaQA | Apache 2.0 | ~2.5 GB | UW NLP / HF |
| OpenAssistant OASST2 | Apache 2.0 | ~200 MB | Hugging Face |

> **Yahoo CQA** is not included — it is only available through Yahoo WebScope (academic registration + non-commercial agreement required).

## Attribution Requirements

All CC BY-SA sources require:
1. Attribution of original URL and author per record
2. Derivative datasets must use the same or compatible CC BY-SA license

Since several sources are CC BY-SA, the combined derived dataset must also be released under CC BY-SA.

## Architecture

```
Raw XML/JSON → Source Parser → CanonicalQA
                                    ├── Normalizer/Cleaner
                                    │       └── Parquet Archive (cold)
                                    │       └── DuckDB (analytics)
                                    ├── Chunker → ChunkRecord
                                    │       └── Embedder → LanceDB (hot vector index)
                                    └── Triple Extractor → Graph Store
```

## Quickstart

```bash
pip install -e ".[dev]"
python -m spacy download en_core_web_sm

# Download a source
data-download stackexchange --sites stackoverflow --limit 10000
data-download squad
data-download openassistant

# Run the full pipeline
data-pipeline run --source stackexchange --chunk-strategy canonical_qa

# Build vector and graph indexes
data-index build --source all
```

## Project Structure

```
data_module/
├── config/           # Per-source and pipeline YAML configs
├── data_module/
│   ├── schema/       # Pydantic models (CanonicalQA, ChunkRecord, Triple)
│   ├── sources/      # Per-source downloaders, parsers, mappers
│   ├── pipelines/    # ETL stages (ingest, transform, chunk, embed, graph)
│   ├── storage/      # Storage backends (Parquet, DuckDB, LanceDB, SQLite, Graph)
│   └── fetch/        # Retrieval APIs (fast_rag, graph_rag, hybrid, agentic)
├── scripts/          # CLI entry points
└── data/             # .gitignored — downloaded and processed data
```

## Storage Backends

- **Parquet** — cold archive, batch reprocessing, fine-tuning datasets
- **DuckDB** — fast SQL analytics over Parquet
- **LanceDB** — hot vector index for fast semantic RAG
- **SQLite** — pipeline state, source → canonical ID mappings
- **NetworkX / Neo4j** — knowledge graph (dev / prod)
