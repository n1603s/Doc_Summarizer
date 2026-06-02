from src.llm import get_llm_client
from src.config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)
from src.prompts import (
    MAP_PROMPT,
    REDUCE_PROMPT
)


client = get_llm_client()


def summarize_chunk(chunk):

    prompt = MAP_PROMPT.format(
        chunk=chunk
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=300
    )

    return response.choices[0].message.content


def generate_final_summary(
    summaries,
    summary_type
):

    joined_summaries = "\n\n".join(
        summaries
    )

    prompt = REDUCE_PROMPT.format(
        summaries=joined_summaries,
        summary_type=summary_type
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content