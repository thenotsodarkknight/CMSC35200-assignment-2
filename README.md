# DLS Lab 2: Domain-Specific Tokenization Analysis

---

## Task Overview

Analysis of BPE tokenization across two distinct text domains:
1. Movie Scripts (12 scripts, 2.85 MB from IMSDB)
2. Python Code (20 files, 1.65 MB from major open-source projects)

---

##  Results

### Movie Scripts
- nanochat: 3.20 bytes/token
- GPT-2: 2.78 bytes/token (15% better)
- cl100k: 3.45 bytes/token (7% worse)
- o200k: 3.46 bytes/token (8% worse)

### Python Code  
- nanochat: 3.89 bytes/token
- GPT-2: 2.43 bytes/token (60% better)
- cl100k: 4.61 bytes/token (16% worse)  
- o200k: 4.59 bytes/token (15% worse)

Finding: Domain-specific tokenizers competitive with 100K+ vocab general tokenizers!

---

## Repository Structure

```
DLS_LAB2_REAL/
├── FINAL_REPORT.md              ← Main deliverable (comprehensive analysis)
├── README.md                     ← This file
├── collect_movie_scripts.py      ← Real data from IMSDB
├── collect_python_code.py        ← Real data from GitHub
├── train_and_analyze_tokenizers.py ← Complete pipeline
├── create_visualizations.py      ← 4 professional figures
├── data/
│   ├── movie_scripts/
│   │   ├── movie_scripts_corpus.txt (2.85 MB, 12 scripts)
│   │   ├── metadata.json
│   │   └── statistics.txt
│   └── python_code/
│       ├── python_code_corpus.txt (1.65 MB, 20 files)
│       ├── metadata.json
│       └── statistics.txt
└── outputs/
    ├── compression_comparison.png
    ├── top_tokens.png
    ├── pattern_distribution.png
    ├── overall_efficiency.png
    ├── tokenizer_analysis_results.json
    ├── movie_scripts_tokenizer/
    └── python_code_tokenizer/
```

---

## Usage

### Data Collection (Already Populated.)
```bash
python3 collect_movie_scripts.py   # 12 real scripts from IMSDB
python3 collect_python_code.py      # 20 files from Flask, Django, etc.
```

### Training & Analysis
```bash
python3 train_and_analyze_tokenizers.py
# Trains both tokenizers, compares with GPT-2/cl100k/o200k
```

### Visualizations
```bash
python3 create_visualizations.py
# Creates 4 professional figures at 300 DPI
```

---


### Domain 1: Movie Scripts

1. Characteristics & Collection 
- 12 real scripts from IMSDB (Pulp Fiction, Matrix, Inception, etc.)
- 2.85 MB, 2,987,814 characters
- Screenplay format: INT/EXT scenes, dialogue, parentheticals
- 1,316 INT scenes, 686 EXT scenes identified

2. Nanochat Tokenizer 
- Trained: 4,096 vocab, 0.31 seconds
- Result: 3.20 bytes/token

3. Standard Tokenizer Comparison 
- GPT-2: 2.78 bytes/token
- cl100k_base: 3.45 bytes/token  
- o200k_base: 3.46 bytes/token

4. Frequent Byte Combinations 
- Top tokens: `\n` (4.68%), `\t\t` (3.81%), `.\n\n` (2.88%)
- Learned: indentation, common words, character names
- Example: `\tMORPHEUS` emerged as single token

5. Discussion 
- Limitations: Format-blind, fragments character names, wastes vocabulary on whitespace
- Patterns Missed: Scene transitions, camera directions, story structure
- Improvements: Parse screenplay format first, hierarchical vocabulary, whitespace normalization

### Domain 2: Python Code

1. Characteristics & Collection 
- 20 files from Flask, Django, NumPy, Pandas, FastAPI, pytest, Black
- 1.65 MB, 1,731,426 characters
- Real production code from GitHub
- 1,148 functions, 239 classes, 706 imports identified

2. Nanochat Tokenizer 
- Trained: 4,096 vocab, 0.21 seconds
- Result: 3.89 bytes/token

3. Standard Tokenizer Comparison 
- GPT-2: 2.43 bytes/token
- cl100k_base: 4.61 bytes/token (worse!)
- o200k_base: 4.59 bytes/token (worse!)

4. Frequent Byte Combinations 
- Top tokens: `       ` (7 spaces, 3.55%), `\n` (2.31%), `,` (1.64%)
- Learned: indentation levels, syntax (`:`, `=`, `.`), keywords (`if`, `None`)
- Mixed code + docstrings = natural language tokens

5. Discussion 
- Limitations: Indentation hell, syntax ignorance, identifier fragmentation, docstring confusion
- Patterns Missed: Import patterns, decorators, comprehensions, type hints, AST structure
- Improvements: AST-based tokenization, indentation normalization, dual-mode (code/prose), identifier-aware vocab

### Visualizations 
- Figure 1: Compression ratio comparison (both domains)
- Figure 2: Top 15 frequent tokens (both domains)
- Figure 3: Token pattern distribution
- Figure 4: Overall efficiency comparison

---

## Main Deliverable

`FINAL_REPORT.md` - Complete analysis with all findings

---

## Data Sources

- Movie Scripts: Internet Movie Script Database (IMSDB) - https://imsdb.com/
- Python Code: GitHub repositories (raw.githubusercontent.com)
  - Flask, Django, Requests, NumPy, Pandas, FastAPI, pytest, Black, scikit-learn

All data publicly available, no authentication required.

