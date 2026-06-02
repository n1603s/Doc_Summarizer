from typing import TypedDict


class SummaryState(TypedDict):

    chunks: list

    summary_type: str

    chunk_summaries: list

    final_summary: str