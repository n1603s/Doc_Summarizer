from concurrent.futures import ThreadPoolExecutor
from typing import Any

from src.state import SummaryState
from src.summarizer import (
    summarize_chunk,
    generate_final_summary
)

try:
    from langgraph.graph import StateGraph, END
    _LANGGRAPH_AVAILABLE = True
except ModuleNotFoundError:
    StateGraph = None  # type: ignore[assignment]
    END = None  # type: ignore[assignment]
    _LANGGRAPH_AVAILABLE = False


def map_node(state: SummaryState) -> dict[str, list[str]]:
    chunks = state["chunks"]

    with ThreadPoolExecutor(max_workers=5) as executor:
        summaries = list(executor.map(summarize_chunk, chunks))

    return {"chunk_summaries": summaries}


def reduce_node(state: SummaryState) -> dict[str, str]:
    final_summary = generate_final_summary(
        summaries=state["chunk_summaries"],
        summary_type=state["summary_type"]
    )

    return {"final_summary": final_summary}


class SimpleSummaryGraph:
    def invoke(self, state: SummaryState) -> dict[str, Any]:
        state = dict(state)
        state.update(map_node(state))
        return reduce_node(state)


def build_summary_graph() -> Any:
    if _LANGGRAPH_AVAILABLE:
        workflow = StateGraph(SummaryState)

        workflow.add_node("map_node", map_node)
        workflow.add_node("reduce_node", reduce_node)
        workflow.set_entry_point("map_node")
        workflow.add_edge("map_node", "reduce_node")
        workflow.add_edge("reduce_node", END)

        return workflow.compile()

    return SimpleSummaryGraph()
