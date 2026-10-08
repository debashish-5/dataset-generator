

```markdown
<div align="center">

# Dataset Generator

**A high-performance Python application and web interface for synthesizing, customizing, and exporting high-fidelity mock datasets.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/framework-Flask-black.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.org/)
[![Data Processing](https://img.shields.io/badge/library-Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

[Key Features](#key-features) • [Repository Structure](#repository-structure) • [Installation](#installation) • [Usage Guide](#usage-guide) • [Schema & Output](#schema--output) • [Contributing](#contributing)

</div>

---

## Overview

**Dataset Generator** streamlines the process of producing synthetic, structured data for machine learning models, system benchmarking, UI testing, and database seeding. It combines a robust Python engine with a web-based interface, enabling both non-technical users and developers to generate schema-compliant dataset exports instantly.

---

## Key Features

* **Schema-Driven Data Generation:** Define custom schemas and specify target row counts to construct realistic synthetic datasets on demand.
* **Interactive Web Interface:** Integrated HTML templates (`templates/`) provide an intuitive dashboard to configure properties and trigger generation visually.
* **Multi-Format Export & Analytics:** Export datasets directly to standard formats like CSV (`phone.csv`) or execute interactive experiments within a Jupyter environment (`test.ipynb`).
* **Extensible API Core:** Modular backend design built on Python, engineered for seamless integration into existing testing pipelines or data engineering workflows.

---

## Repository Structure

```text
dataset-generator/
├── templates/              # HTML frontend templates for web generation interface
├── dataset_genrator.py     # Core Python API engine and web server application
├── phone.csv               # Sample exported synthetic dataset output
├── test.ipynb              # Jupyter notebook for interactive testing and schema prototyping
└── .vscode/                # IDE configurations and environment settings

```

---

## Technical Stack

* **Language:** Python 3.8+
* **Backend Framework:** Flask / FastAPI
* **Data Processing Engine:** Pandas, NumPy
* **Interactive Environment:** Jupyter Notebook / Lab

---

## Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/debashish-5/dataset-generator.git](https://github.com/debashish-5/dataset-generator.git)
cd dataset-generator

```

### 2. Configure Virtual Environment

```bash
# On Linux/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install pandas notebook flask

```

---

## Usage Guide

### Starting the Web Dashboard

Launch the web backend to interact with the visual interface:

```bash
python dataset_genrator.py

```

Once running, access the user interface by navigating to `http://localhost:5000` in your web browser.

### Interactive Prototyping

For schema testing, exploratory data analysis, or custom generation script development, open the included Jupyter notebook:

```bash
jupyter notebook test.ipynb

```

---

## Schema & Output Example

Sample output generated using default product specification schemas (`phone.csv`):

| Product ID | Product Name | Category | Hardware Specifications | Price (USD) | Availability |
| --- | --- | --- | --- | --- | --- |
| `DEV-1092` | Flagship Phone X | Mobile | 256GB / 12GB RAM | $899.00 | In Stock |
| `DEV-1093` | Lite Phone Pro | Mobile | 128GB / 8GB RAM | $499.00 | In Stock |
| `DEV-1094` | Budget Phone A1 | Mobile | 64GB / 4GB RAM | $199.00 | Out of Stock |

---

## Roadmap & Future Enhancements

* **JSON & Parquet Exports:** Support for binary and unstructured data output formats.
* **Constraint Validation Engine:** Custom rule enforcement for logical value generation (e.g., date sequence validation, range limits).
* **Faker Integration:** Expanded domain-specific data providers (geographic, personal identifiable information, financial metrics).

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
