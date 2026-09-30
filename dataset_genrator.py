from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Literal
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import pandas as pd
from flask import Flask,render_template,request,jsonify
import requests
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "generated_datasets"
DATASET_DIR.mkdir(exist_ok=True)


def clean_filename(filename: str) -> str:
    """
    Makes sure the filename is safe and ends with .csv
    """

    filename = Path(filename).name

    # Remove unwanted characters
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    return filename


class Dataset(BaseModel):
    file_name:str = Field(description="For Dataset Name (csv file format allowed only, Example: 'data.csv')")
    columns:list[str] = Field(description="Name of the columns for dataset generator , if user don't give the columns name you can take columns by own.")
    data: list[list] = Field(description="Data/rows for creating dataset")


def generate_dataset(query:str,filepath:str | None = None) -> str:
    prompt = f"""
    You are a professional synthetic dataset generator.

    User request:
    {query}

    Requirements:

    1. Generate best data.
    2. Create useful and realistic synthetic data.
    3. Decide suitable column names if the user did not specify them.
    4. Every row must have exactly the same number of values as the columns.
    5. Return structured data only.
    6. The output must be suitable for saving as a CSV file.
    7. Use this filename:

    """
    query = prompt.invoke({'query':query})


    model = ChatOllama(model = "mistral")
    structured_model = model.with_structured_output(Dataset)
    generator = structured_model.invoke(query)
    if not generator.columns:
        raise ValueError("The Model did not generate any columns.")
    if not generator.data:
        raise ValueError("The Model did not generate any data")
    for row in generator.data:
        if len(row) != len(generator.columns):
            raise ValueError("Generate rows do not match with the number of columns")
        
    df = pd.DataFrame(data=generator.data, columns=generator.columns)
    if not filepath:
        filepath = generator.file_name
    
    filepath = BASE_DIR /filepath
    df.to_csv(filepath, index = False)
    return {
        "file_name": filepath,
        "file_path": str(filepath),
        "columns": generator.columns,
        "data": df.astype(str).values.tolist(),
        "rows": len(df),
        "columns_count": len(df.columns)
    }



app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/generate", methods=["POST"])
def generate_api():

    try:

        payload = request.get_json(silent=True) or {}


        query = (
            payload.get("query")
            or payload.get("prompt")
            or "Generate 5 sample product details for mobile phones."
        )

        filename = (
            payload.get("filename")
            or "dataset.csv"
        )

        rows = payload.get("rows") or 5


        try:
            rows = int(rows)

        except (TypeError, ValueError):

            rows = 5


        result = generate_dataset(
            query=query,
            filename=filename,
            rows=rows
        )



        return jsonify({
            "status": "success",
            "message": (
                f"Dataset generated successfully: "
                f"{result['file_name']}"
            ),
            "file_name": result["file_name"],
            "rows": result["rows"],
            "columns_count": result["columns_count"],
            "columns": result["columns"],
            "data": result["data"]
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/click", methods=["POST"])
def click_handler():

    return generate_api()


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )