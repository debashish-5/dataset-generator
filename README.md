
# Dataset Generator

A lightweight Python web application and tool for generating, customizing, and exporting synthetic datasets (such as product specs, phone details, and mock data) for machine learning, testing, and data analysis.

---

## 🚀 Features

- **Custom Dataset Generation:** Specify row counts and data schema to generate custom synthetic data on the fly.
- **Web Interface:** Built-in web frontend templates (`templates/`) to configure and trigger dataset generation directly from your browser.
- **CSV & Jupyter Integration:** Export generated outputs straight to CSV format (`phone.csv`) or test generation scripts interactively using the included Jupyter notebook (`test.ipynb`).
- **Flexible API Backend:** Python-backed dataset generation API ready for customization and scaling.

---

## 📁 Repository Structure

```text
dataset-generator/
├── templates/              # HTML frontend templates for the web interface
├── dataset_genrator.py     # Main Python backend script/API logic
├── phone.csv               # Sample exported dataset file
├── test.ipynb              # Jupyter notebook for interactive testing & experimentation
└── .vscode/                # VS Code workspace and Python environment configuration

```

---

## 🛠️ Getting Started

### Prerequisites

* **Python 3.8+** installed on your system.
* Standard Python libraries (e.g., `pandas`, `flask`/`fastapi` depending on your web frame).

### Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/debashish-5/dataset-generator.git](https://github.com/debashish-5/dataset-generator.git)
cd dataset-generator

```


2. **Set up a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install pandas notebook flask

```



---

## 💻 Usage

### Running the Web Application

To launch the generation interface:

```bash
python dataset_genrator.py

```

Open your browser and navigate to `http://localhost:5000` (or the port specified in terminal output) to start generating datasets.

### Using the Notebook

For rapid testing and data exploration, launch the included Jupyter Notebook:

```bash
jupyter notebook test.ipynb

```

---

## 📄 Example Output

Sample datasets generated with header metadata and product specifications are saved as `.csv` files (e.g., `phone.csv`):

| Product Name | Category | Spec Detail | Price |
| --- | --- | --- | --- |
| Sample Phone | Mobile | 128GB / 8GB RAM | $599 |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [Issues page](https://github.com/debashish-5/dataset-generator/issues) if you want to contribute.

---

## 📜 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```

```
