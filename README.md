# JARVIS — Local LLM Assistant on CPU-Only Hardware

A fully local AI assistant built on **Qwen2.5 7B Instruct**, running entirely
on CPU without a dedicated GPU and within a 16 GB RAM budget. Supports natural
language queries, RAG over private documents, and external tool calling via
Ollama's native function-calling schema.

**Demo Video:** [https://youtu.be/TFvDtzko88Y]

---

## Requirements

Before running the project, make sure your system meets the following:

| Requirement | Minimum |
|---|---|
| Operating System | Windows 10/11, Ubuntu 20.04+, or macOS 12+ |
| RAM | 16 GB (32 GB recommended for Q8_0) |
| Free Disk Space | 15 GB (for models + corpus) |
| Python | 3.10 or higher |
| Git | Any recent version |
| Ollama | v0.2.x or higher |

---

## Step 1 — Install Ollama

Download and install Ollama from the official site:

https://ollama.com/download

After installation, verify it works:

```bash
ollama --version
```

Keep Ollama running in the background before executing any script.

---

## Step 2 — Download the Required Models

Open a terminal and run the following commands:

```bash
# Main inference model — REQUIRED (4.7 GB)
ollama pull qwen2.5:7b-instruct-q4_K_M

# Embeddings model for RAG — REQUIRED (274 MB)
ollama pull nomic-embed-text
```

### Optional models (for benchmark comparison only):

```bash
# High-quality version — 8-bit (7.7 GB)
ollama pull qwen2.5:7b-instruct-q8_0

# High-speed version — 3-bit (3.5 GB)
ollama pull qwen2.5:7b-instruct-q3_K_M
```

Verify all downloaded models:

```bash
ollama list
```

---

## Step 3 — Clone the Repository and Install Dependencies

```bash
git clone https://github.com/YOUR_GITHUB_USER/JARVIS_PROJECT.git
cd JARVIS_PROJECT
pip install -r requirements.txt
```

This installs all required Python packages:

| Package | Version | Purpose |
|---|---|---|
| ollama | >=0.2.0 | Python client for the Ollama API |
| chromadb | >=0.4.0 | Vector database for RAG |
| duckduckgo-search | >=5.0 | Web search backend |
| psutil | >=5.9.0 | RAM and CPU monitoring |
| requests | >=2.31.0 | HTTP communication with REST API |

---

## Step 4 — Set Up the RAG Corpus

Place the file `MANUAL-DE-MECANICA-BASICA.pdf` inside the `data/corpus/` folder:

```
JARVIS_PROJECT/
└── data/
    └── corpus/
        └── MANUAL-DE-MECANICA-BASICA.pdf   ← place it here
```

The vector index is built automatically the first time `rag_pipeline.py` is
invoked. The generated index is stored in `data/chroma_db/` and does not need
to be rebuilt on subsequent runs.

---

## Step 5 — Run the System

All scripts are executed from the `src/` folder:

```bash
cd src
```

### Start Jarvis in interactive mode:
```bash
python mcp_main.py
```

### Run quantization benchmark (Part A):
```bash
python benchmark.py
```
Results saved to → `data/measurements.csv`

### Measure KV Cache impact by context length (Part B):
```bash
python kv_q8_test.py
```

### Run full automated evaluation (Part E):
```bash
python evaluator.py
```
Results saved to → `data/eval_results.json`

### Generate result plots:
Open and run all cells in:
```
notebooks/plots.ipynb
```
Plots saved to → `report/`

---

## Repository Structure

```
JARVIS_PROJECT/
├── data/
│   ├── chroma_db/
│   │   └── chroma.sqlite3       # ChromaDB vector index (auto-generated)
│   ├── corpus/
│   │   └── MANUAL-DE-MECANICA-BASICA.pdf   # Automotive mechanics corpus
│   ├── eval_results.json        # Automated evaluation results
│   ├── measurements.csv         # Benchmark metrics per quantization
│   └── test_set.json            # Set of 20 evaluation prompts
├── notebooks/
│   └── plots.ipynb              # Result plot generation
├── report/
│   ├── 1_velocidad_tokens.png
│   ├── 2_consumo_ram.png
│   ├── 3_impacto_contexto.png
│   ├── 4_tamano_archivo.png
│   ├── 5_latencia_preguntas.png
│   ├── 6_tasa_exito.png
│   └── jarvis_ieee.pdf          # Final technical report (IEEE format)
├── src/
│   ├── __pycache__/
│   │   └── mcp_tools.cpython-311.pyc
│   ├── benchmark.py             # Quantization benchmark (Part A)
│   ├── evaluator.py             # Automated evaluation (Part E)
│   ├── kv_q8_test.py            # KV Cache tests (Part B)
│   ├── mcp_main.py              # Main entry point
│   ├── mcp_tools.py             # External tools (web search, file system)
│   └── rag_pipeline.py          # RAG pipeline with ChromaDB
├── README.md
└── requirements.txt
```

---

## AI Assistance Declaration

This project was developed with the complementary assistance of two AI systems:

- **Google Gemini** — used for: source code generation and structuring, response
  evaluation and scoring with the 0–3 rubric, and generation of result plots.
- **Claude (Anthropic)** — used for: drafting and structuring this README and
  the technical report in IEEE format, critical analysis of results, correction
  of `requirements.txt`, classification of the 20 evaluation results.

All numerical data, empirical measurements, and analyses derive from hardware
and experiments operated locally by the author.

---

## Author

**José Alexander Quishpe Reinoso**  
Universidad Internacional del Ecuador (UIDE)  
joquishpere@uide.edu.ec