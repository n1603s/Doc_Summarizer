import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 5

TEMPERATURE = 0.2

MAX_TOKENS = 800

TOP_K = 5

SUMMARY_OPTIONS = {
    "Short": 150,
    "Medium": 300,
    "Detailed": 600
}