MAP_PROMPT = """
You are an expert document summarizer.

Your task is to summarize the following
document chunk.

Focus only on key information.

Document Chunk:

{chunk}
"""

REDUCE_PROMPT = """
You are an expert document summarizer.

You are given summaries from multiple sections
of the same document.

Generate a final summary.

Summary Type:
{summary_type}

Rules:

Short:
150 words maximum

Medium:
300 words maximum

Detailed:
600 words maximum

Chunk Summaries:

{summaries}
"""

RAG_PROMPT = """
Answer the question using ONLY the context.

Context:
{context}

Question:
{question}

If the answer is not present,
say:

'I could not find that information
in the document.'
"""