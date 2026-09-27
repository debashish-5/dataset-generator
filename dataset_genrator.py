from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Literal
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import pandas as pd
from flask import Flask,render_template,request
import requests

class Dataset(BaseModel):
    file_name:str = Field(description="For Dataset Name (csv file format allowed only, Example: 'data.csv')")
    columns:list[str] = Field(description="Name of the columns for dataset generator , if user don't give the columns name you can take columns by own.")
    data: list[list] = Field(description="Data/rows for creating dataset")


def generate_dataset(query:str,filepath:str = None) -> str:
    model = ChatOllama(model = "mistral")
    structured_model = model.with_structured_output(Dataset)
    generator = structured_model.invoke(query)
    df = pd.DataFrame(data=generator.data, columns=generator.columns)
    if not filepath:
        df.to_csv(generator.file_name,index=False)
        return "Data created & Saved Successfully"

    df.to_csv(filepath, index = False)
    return "Data created & Saved Successfully"




app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_api():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query") or payload.get("prompt") or "Generate 5 sample product details for mobile phones."
    result = generate_dataset(query=query)
    return {'status':'success','message':result}



@app.route("/click", methods=["POST"])
def click_handler():
    return generate_api()


if __name__ == "__main__":
    app.run(debug=True)



    