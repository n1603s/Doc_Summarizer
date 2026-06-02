from openai import OpenAI

from src.config import (
    OPENROUTER_API_KEY
)


def get_llm_client():

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )