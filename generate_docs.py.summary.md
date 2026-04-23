# File: generate_docs.py

## Purpose
This script generates documentation for a repository by summarizing the content of its files and writing it to Markdown files.

## Key Components
- `process_repo(root)`: Walks through a repository, summarizes each file, and writes the summaries to individual Markdown files.
- `summarize_file(filepath)`: Uses the LLaMA model to generate a summary of a given file's content in Markdown format.
- `bootstrap_from_file_list(file_list_path)`: Reads a list of files from a file, processes them using `process_repo`, and saves the state to `.docs_state.json`.

## Important Logic
The script uses a state file (`".docs_state.json"`) to keep track of which files have been processed. If a file's content hasn't changed since the last run, it is skipped.

## Dependencies
- Python `requests` library for making API calls to LLaMA model
- `hashlib` library for computing SHA256 hashes of file contents
- LLaMA model (`OLLAMA_URL`, `MODEL`) must be set up and accessible

## Notes
- This script assumes the repository structure is standard, with files organized in subdirectories.
- The script generates Markdown files with summaries for each file. These can be used to generate a table of contents or README files.