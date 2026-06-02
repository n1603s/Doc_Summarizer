from src.llm import get_llm_client

from src.config import (
    MODEL_NAME,
    TOP_K,
    TEMPERATURE
)

from src.prompts import (
    RAG_PROMPT
)


client = get_llm_client()


def answer_question(
    vectorstore,
    question
):

    docs = vectorstore.similarity_search(
        question,
        k=TOP_K
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
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
        max_tokens=500
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    return answer, docs