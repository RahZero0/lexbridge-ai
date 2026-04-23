import os
import requests
import hashlib
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"
STATE_FILE = ".docs_state.json"
FORCE = False

ALLOWED_EXT = {".py", ".ts", ".js", ".yaml", ".yml", ".toml", ".sh"}

IGNORE_DIRS = {
    # Python
    "venv", ".venv", ".env",
    "__pycache__", ".mypy_cache", ".pytest_cache",

    # Node / pnpm
    "node_modules",
    ".pnpm",
    ".turbo",
    ".next",
    ".nuxt",
    "dist",
    "build",

    # Git / misc
    ".git",
    ".idea",
    ".vscode"
}

IGNORE_FILES = {
    "generate_docs.py",
    "RAG_LAYOUT_REVIEW.md",
    ".docs_state.json",
    ".DS_Store",
}

IGNORE_EXT = {
    ".md",
    ".png", ".jpg", ".jpeg", ".gif", ".mp4",
    ".parquet", ".csv", ".db", ".sqlite",
    ".lock",
    ".min.js", ".map"
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            raw = json.load(f)
            return {os.path.abspath(k): v for k, v in raw.items()}
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def normalize_path(path):
    return os.path.abspath(path)

def should_skip(path):
    filename = os.path.basename(path)
    ext = os.path.splitext(filename)[1].lower()
    parts = set(path.split(os.sep))

    if parts & IGNORE_DIRS:
        return True

    if filename.startswith("."):
        return True

    if ext not in ALLOWED_EXT:
        return True

    return False

def bootstrap_from_file_list(file_list_path):
    state = {}

    with open(file_list_path, "r") as f:
        files = [line.strip() for line in f if line.strip()]

    for path in files:
        full_path = normalize_path(path)

        if not os.path.exists(full_path):
            print(f"Missing: {full_path}")
            continue

        if should_skip(full_path):
            continue

        file_hash = get_file_hash(full_path)
        if not file_hash:
            continue

        state[full_path] = file_hash
        print(f"Added: {full_path}")

    save_state(state)
    print(f"\n✅ Loaded {len(state)} files into state")


def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        # DEBUG: print full response if needed
        if "response" not in data:
            print("⚠️ Unexpected Ollama response:")
            print(data)
            return None

        return data["response"]

    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return None


def summarize_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return None

    if not content.strip():
        return None

    prompt = f"""
You are a code summarizer.

Summarize the following file.

ONLY return markdown in this format:

# File: {os.path.basename(filepath)}

## Purpose
## Key Components
## Important Logic
## Dependencies
## Notes

File content:
{content[:8000]}
"""
    if os.path.basename(filepath) in {
        "package.json", "pyproject.toml", "pnpm-workspace.yaml"
    }:
        prompt += "\n\nThis is a configuration file. Explain dependencies and structure clearly."

    return call_ollama(prompt)


def process_repo(root):
    state = load_state()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        summaries = []

        for file in filenames:
            full_path = normalize_path(os.path.join(dirpath, file))

            if should_skip(full_path):
                continue

            file_hash = get_file_hash(full_path)
            if not file_hash:
                continue

            # 🔥 SKIP if unchanged
            if state.get(full_path) == file_hash:
                print(f"Skipping unchanged: {full_path}")
                continue

            print(f"Processing {full_path}")

            summary = summarize_file(full_path)

            if summary:
                summary_file = full_path + ".summary.md"
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write(summary)

                summaries.append((file, summary))

                # ✅ update state
                state[full_path] = file_hash

        # write README if needed
        if summaries:
            readme_path = os.path.join(dirpath, "README.md")

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# Folder: {os.path.basename(dirpath)}\n\n")
                f.write("## Files\n")

                for file, summary in summaries:
                    lines = summary.split("\n")
                    desc = lines[2] if len(lines) > 2 else ""
                    f.write(f"- {file} → {desc}\n")

    save_state(state)


if __name__ == "__main__":
    import sys

    if "--bootstrap" in sys.argv:
        bootstrap_from_file_list("processed_files.txt")  # 👈 your file
    else:
        process_repo(".")
