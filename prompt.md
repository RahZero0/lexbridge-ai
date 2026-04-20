# Claude Code Prompt for Repository Summarization

You are an expert codebase analyzer and documentation generator.

## GOAL
Create a documentation layer that allows an LLM to understand the entire codebase without reading raw code.

---

## RULES

### 1. DIRECTORY TRAVERSAL
- Recursively walk through all folders
- Ignore:
  - __pycache__ folders
  - node_modules
  - .git
  - build/dist folders
  - binary files
  - large data files (csv, parquet, db, lance, etc.)
- Only process meaningful source files and configs

---

### 2. FILE SUMMARIZATION

For each file create:
<original_filename>.summary.md

Content format:

# File: <filename>

## Purpose
(What this file does)

## Key Components
(functions, classes, modules with 1-line explanation each)

## Important Logic
(core logic explained simply)

## Dependencies
(imports and interactions)

## Notes
(any important design decisions or quirks)

---

### 3. FOLDER SUMMARY

For EACH folder, create README.md

# Folder: <folder_name>

## Overview
(What this folder is responsible for)

## Files
- file1 → short description
- file2 → short description

## Subfolders
- subfolder1 → what it contains + link to its README

## Relationships
(How this folder connects to others)

## Key Flows
(optional: describe important pipelines or flows)

---

### 4. NESTED LINKING
- If a folder contains subfolders:
  - DO NOT inline their details
  - Instead link to their README.md

Example:
See: ../retrieval/README.md

---

### 5. GLOBAL INDEX

Create CODEBASE_SUMMARY.md

# Codebase Summary

## High-Level Architecture
(big picture system design)

## Core Modules
(list major folders and their roles)

## Data Flow
(step-by-step system flow)

## Entry Points
(main scripts / APIs)

## How to Navigate
(instructions for an LLM to use this documentation)

---

### 6. STYLE
- Be concise but informative
- No fluff
- Prefer bullet points
- Optimize for LLM retrieval

---

### 7. OUTPUT LOCATION

Option A:
file.py → file.py.summary.md

Option B (preferred):
/docs/<mirrored_structure>/

---

### 8. SPECIAL HANDLING
- Skip large data directories
- Focus on core logic modules

---

### 9. FINAL STEP

Create LLM_INSTRUCTIONS.md

You are querying a summarized codebase.

ALWAYS:
1. Start from CODEBASE_SUMMARY.md
2. Navigate to relevant folder README.md
3. Drill down into file summaries

DO NOT:
- Read raw code unless necessary
- Assume behavior without checking summaries

Use the documentation hierarchy as the source of truth.

---

## EXECUTION STRATEGY

1. Traverse repo
2. Summarize files
3. Build folder READMEs
4. Link everything
5. Generate global summary
