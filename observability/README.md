# Data Observatory (v1)

A unified dashboard to visualize data across the project storage backends:

- Parquet + DuckDB (dataset analytics)
- SQLite (pipeline state and checkpoints)
- LanceDB (vector index health)
- NetworkX graph snapshot (local graph exploration)

## Run

From repo root:

```bash
pip install -r observability/requirements.txt
streamlit run observability/dashboard.py
```

First run can show Streamlit onboarding/telemetry prompt. This repo now includes `.streamlit/config.toml` with telemetry disabled and quieter logs.
You can still override from CLI:

```bash
streamlit run observability/dashboard.py --browser.gatherUsageStats false
```

## What you get

- Global filters (source, language, year)
- KPI cards for canonical/chunk/vector/graph/pipeline volume
- Dataset charts (source mix, source-year heatmap, top tags, score buckets, interactive scatter explorer)
- Pipeline run history + status/source mix + duration and throughput visuals from SQLite
- Vector index profiling (LanceDB + chunk metadata heatmaps, token spread, chunking policy treemap)
- Graph metrics, relation-mix chart, and neighborhood explorer with selectable layout engine
- SQL explorer for ad-hoc DuckDB queries

## Notes

- The app reads storage paths from `data_module/config/storage.yaml`.
- If a backend is missing locally (for example no graph file yet), the dashboard degrades gracefully and shows a hint instead of failing.
- Graph analytics is lazy by default (toggle in the Graph tab) so startup remains fast even with large graph files.
