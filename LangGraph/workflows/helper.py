from IPython.display import Image
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
import os
import json
import re

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

a = 5

def model(model_name="gemini-2.5-flash"):
  return genai.GenerativeModel(model_name)

def extract_and_validate(response, schema_class: type[BaseModel]) -> BaseModel:
    """
    Extracts JSON from a model response and validates it against the provided Pydantic schema.
    
    Args:
        response: LLM response object with `.text` attribute.
        schema_class: A Pydantic model class (e.g., TweetEvaluation, EssayFeedbackSchema).
    
    Returns:
        An instance of the validated schema.
    """
    raw_output = response.text.strip()

    def extract_json(text: str) -> str:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        return match.group(1) if match else text.strip()

    clean_json = extract_json(raw_output)

    try:
        parsed = json.loads(clean_json)
        return schema_class(**parsed)
    except Exception as e:
        raise ValueError(f"Validation failed.\nError: {e}\nRaw output:\n{repr(clean_json)}")

def draw_graph(workflow_name):
  return Image(workflow_name.get_graph().draw_mermaid_png())