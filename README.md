# Dataset Generator

**Agentic Synthetic Data Synthesis Platform Powered by Local LLMs, LangChain, and LangSmith Observability**

---

[Architectural Overview](https://www.google.com/search?q=%23architectural-overview) • [System Flow & Tracing](https://www.google.com/search?q=%23system-flow--tracing) • [Codebase Walkthrough](https://www.google.com/search?q=%23codebase-walkthrough) • [Repository Directory](https://www.google.com/search?q=%23repository-directory) • [Installation & Setup](https://www.google.com/search?q=%23installation--setup) • [API Protocol](https://www.google.com/search?q=%23api-protocol) • [Troubleshooting & Validation](https://www.google.com/search?q=%23troubleshooting--validation)

---

## Technical Overview

**Dataset Generator** is an agentic synthetic data creation system that leverages local large language models via **LangChain** and **Ollama**, enforced by **Pydantic** structured schemas, and fully monitored through **LangSmith** observability tracing.

Unlike simple random data mock generators, this system utilizes context-aware generative AI (`Mistral` LLM) to produce schema-accurate, domain-specific tabular datasets on demand. The architecture exposes a **Flask REST API** and client-side web interface for web generation, alongside a **Jupyter Notebook workspace** (`test.ipynb`) for schema prototyping.

---

## Architectural Overview

The core generation pipeline decouples prompt orchestration from output verification using Pydantic structured output models (`Dataset`). The execution graph follows an end-to-end traced workflow:

```text
+-----------------------------------------------------------------------------------+
|                                 CLIENT LAYER                                      |
|                                                                                   |
|    +--------------------------+                      +-----------------------+    |
|    |   Web UI (index.html)    |                      |   Jupyter Notebook    |    |
|    |   HTTP POST /generate    |                      |     (test.ipynb)      |    |
|    +------------+-------------+                      +-----------+-----------+    |
+-----------------|------------------------------------------------|----------------+
                  |                                                |
                  v                                                v
+-----------------------------------------------------------------------------------+
|                          FLASK BACKEND CONTROLLER LAYER                           |
|                                                                                   |
|    +-------------------------------------------------------------------------+    |
|    |                         dataset_genrator.py                             |    |
|    |                                                                         |    |
|    |   [ Home Route: / ]    [ API Endpoint: /generate ]   [ Handler: /click ]|    |
|    +------------------------------------+------------------------------------+    |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        LANGCHAIN & LLM ENGINE LAYER                               |
|                                                                                   |
|    +-------------------------------------------------------------------------+    |
|    |                     generate_dataset() Generator                        |    |
|    |                                                                         |    |
|    |  1. Prompt Builder (System Instructions + User Prompt + Row Constraints)|    |
|    |  2. ChatOllama(model="mistral") Engine                                  |    |
|    |  3. Structured Output Binding (.with_structured_output(Dataset))        |    |
|    +------------------------------------+------------------------------------+    |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     VALIDATION & DATA PROCESSING ENGINE                           |
|                                                                                   |
|    +-------------------------------------------------------------------------+    |
|    |  Pydantic Model (Dataset):                                              |    |
|    |  - file_name: str                                                       |    |
|    |  - columns: list[str]                                                   |    |
|    |  - data: list[list]                                                     |    |
|    |                                                                         |    |
|    |  Parity Verification: len(row) == len(columns) for all rows             |    |
|    |  Filename Sanitizer: clean_filename() (Regex safety + .csv enforce)     |    |
|    |  Pandas DataFrame Construction: pd.DataFrame(data, columns)             |    |
|    +------------------------------------+------------------------------------+    |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     PERSISTENCE & OBSERVABILITY LAYER                             |
|                                                                                   |
|    +----------------------------------+   +----------------------------------+    |
|    |       Disk Storage System        |   |       LangSmith Tracing          |    |
|    |   BASE_DIR / generated_datasets  |   |   @traceable decoratored runs    |    |
|    |   Exported CSV Output File       |   |   Execution metrics & latency    |    |
|    +----------------------------------+   +----------------------------------+    |
+-----------------------------------------------------------------------------------+

```

---

## System Flow & Tracing

The generation process uses strict validation gates to guarantee tabular integrity:

```text
User Payload ──> [Flask API Controller]
                       │
                       ▼
            [@traceable: "Dataset Generator"]
                       │
                       ├──> Construct System Context & User Query Prompt
                       │
                       ├──> Invoke ChatOllama("mistral") via Structured Output
                       │
                       ├──> Validate Non-Empty Columns & Data Matrices
                       │
                       ├──> Verify Row-to-Column Length Matching
                       │
                       ├──> [@traceable: "Clean File Name"] Sanitization
                       │
                       ├──> Construct Pandas DataFrame & Export CSV to Disk
                       │
                       └──> Return JSON Payload (Columns, Matrix, Row Count)

```

### Observability Tracing Wrappers

LangSmith tracing is integrated across function boundaries using `@traceable`:

* `@traceable(name="Clean File Name")`: Tracks string sanitization performance and regex execution.
* `@traceable(name="Dataset Generator")`: Monitors LLM token generation latency, schema parsing success, and matrix integrity checks.
* `@traceable(name="Home")`: Logs landing page visits.
* `@traceable(name="GENERATE API")`: Logs REST API requests, status payload outputs, and runtime exceptions.
* `@traceable("Click Handler")`: Monitors user interaction handlers.

---

## Codebase Walkthrough

### 1. Pydantic Structured Data Schema

The model enforces structured tabular outputs directly from the LLM engine:

```python
class Dataset(BaseModel):
    file_name: str = Field(
        description="Analyze user goal and choose a suitable dataset filename (CSV format only, e.g., 'data.csv')."
    )
    columns: list[str] = Field(
        description="List of column names. If unspecified by user, infer appropriate names automatically."
    )
    data: list[list] = Field(
        description="Two-dimensional matrix representing row values for the generated dataset."
    )

```

### 2. File Name Sanitizer Engine

Removes unsafe characters and ensures proper `.csv` extension attachment:

```python
@traceable(name="Clean File Name")
def clean_filename(filename: str) -> str:
    filename = Path(filename).name
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    return filename

```

### 3. Core Synthesis Function (`generate_dataset`)

Constructs the LLM prompt, binds the Pydantic schema, executes structured inference via Ollama, validates column-row parity, builds a Pandas DataFrame, and saves the file:

```python
@traceable(name="Dataset Generator")
def generate_dataset(query: str, filepath: str | None = None, rows: int = 5) -> dict:
    prompt = f"""
    You are a professional synthetic dataset generator.

    User request:
    {query}

    Requirements:
    1. Generate best data.
    2. Create useful and realistic synthetic data.
    3. Decide suitable column names if the user did not specify them.
    4. Every row must have exactly the same number of values as the columns.
    5. Generate exactly {rows} rows.
    6. Return structured data only.
    7. The output must be suitable for saving as a CSV file.
    """

    model = ChatOllama(model="mistral")
    structured_model = model.with_structured_output(Dataset)
    generator = structured_model.invoke(prompt)

    # Matrix integrity verification
    if not generator.columns:
        raise ValueError("The Model did not generate any columns.")
    if not generator.data:
        raise ValueError("The Model did not generate any data.")
    for row in generator.data:
        if len(row) != len(generator.columns):
            raise ValueError("Generated row length does not match column count.")

    df = pd.DataFrame(data=generator.data, columns=generator.columns)
    if not filepath:
        filepath = generator.file_name

    filepath_full = BASE_DIR / filepath
    df.to_csv(filepath_full, index=False)
    
    return {
        "file_name": filepath,
        "file_path": str(filepath_full),
        "columns": generator.columns,
        "data": df.astype(str).values.tolist(),
        "rows": len(df),
        "columns_count": len(df.columns)
    }

```

---

## Repository Directory

```text
dataset-generator/
│
├── generated_datasets/         # Target output directory for dynamically built CSVs
├── templates/                  # Web interface template assets
│   └── index.html              # Interactive client UI dashboard
│
├── .vscode/                    # Workspace & Python interpreter environment configurations
├── .env                        # Environment variables (API Keys, LangSmith settings)
├── .gitignore                  # Git tracking exclusion rules
├── dataset_genrator.py         # Main Flask server, LangChain LLM generator, and API
├── phone.csv                   # Sample dataset output artifact (mobile product specs)
├── udemy.csv                   # Sample dataset output artifact (course data)
└── test.ipynb                  # Interactive Jupyter notebook for prototyping & testing

```

---

## Installation & Setup

### Prerequisites

1. **Python:** 3.8 or higher installed.
2. **Ollama:** Installed locally and running.
```bash
ollama pull mistral

```



### 1. Clone Repository

```bash
git clone https://github.com/debashish-5/dataset-generator.git
cd dataset-generator

```

### 2. Configure Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# Or install core libraries manually:
pip install pydantic typing_extensions langchain-groq langchain-ollama pandas flask requests langsmith python-dotenv notebook

```

### 4. Configure Environment Variables (`.env`)

Create a `.env` file in the project root:

```env
# LangSmith Observability Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
LANGCHAIN_PROJECT="dataset-generator"

# Optional Cloud LLM Backup Keys
GROQ_API_KEY="your_groq_api_key_here"

```

---

## Running the Application

### Option A: Launch Flask Web Application

Start the server backend:

```bash
python dataset_genrator.py

```

Open your browser and navigate to:
`[http://127.0.0.1:5000](http://127.0.0.1:5000)`

### Option B: Interactive Prototyping in Jupyter

Launch the testing workspace notebook:

```bash
jupyter notebook test.ipynb

```

---

## API Protocol

### Endpoint: `POST /generate`

Generates a synthetic dataset according to prompt criteria and saves the resulting CSV file locally.

#### Request Headers

```http
Content-Type: application/json

```

#### Request Payload

```json
{
  "query": "Generate 5 sample details of gaming laptops including model, GPU, RAM, and price.",
  "filename": "laptops.csv",
  "rows": 5
}

```

#### Success Response (`200 OK`)

```json
{
  "status": "success",
  "message": "Dataset generated successfully: laptops.csv",
  "file_name": "laptops.csv",
  "rows": 5,
  "columns_count": 4,
  "columns": ["Laptop Model", "GPU", "RAM", "Price (USD)"],
  "data": [
    ["Asus ROG Strix", "NVIDIA RTX 4080", "32GB", "$2199"],
    ["MSI Raider GE78", "NVIDIA RTX 4090", "64GB", "$3299"],
    ["Lenovo Legion Pro 7i", "NVIDIA RTX 4070", "16GB", "$1749"],
    ["Acer Predator Helios", "NVIDIA RTX 4060", "16GB", "$1399"],
    ["Razer Blade 16", "NVIDIA RTX 4090", "32GB", "$3599"]
  ]
}

```

#### Error Response (`500 Internal Server Error`)

```json
{
  "status": "error",
  "message": "Generated row length does not match column count."
}

```

---

## Troubleshooting & Validation

| Issue | Root Cause | Solution |
| --- | --- | --- |
| **`ConnectionRefusedError` on Ollama** | Ollama local daemon is not running. | Execute `ollama serve` or launch the Ollama app desktop process. |
| **`ValueError: Model did not generate data`** | LLM output was cut off or failed schema parsing. | Ensure the model `mistral` is pulled (`ollama pull mistral`) and check system RAM limits. |
| **Missing Traces in LangSmith** | `LANGCHAIN_TRACING_V2` or API Key missing in `.env`. | Verify `.env` parameters and ensure `load_dotenv()` runs before importing LangChain modules. |
| **Filename Overwriting / Misformatting** | Non-standard string passed in filename argument. | The internal `clean_filename()` method automatically strips invalid characters and enforces `.csv` extensions. |

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.
