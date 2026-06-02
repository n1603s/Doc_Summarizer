import time
import tempfile

import streamlit as st

from src.loader import load_pdf
from src.splitter import split_documents
from src.embeddings import get_embeddings
from src.vector_store import create_vectorstore

from src.graph import build_summary_graph

from src.rag_qa import answer_question

from src.export import save_summary


st.set_page_config(
    page_title="Document Summarization Assistant",
    page_icon="📄",
    layout="wide"
)

st.title(
    "📄 Document Summarization & RAG Assistant"
)

st.markdown(
    """
Upload a PDF document, generate summaries,
and ask questions about the document.
"""
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(
            uploaded_file.read()
        )

        pdf_path = tmp.name

    with st.spinner(
        "Processing document..."
    ):

        documents = load_pdf(
            pdf_path
        )

        chunks = split_documents(
            documents
        )

        embeddings = get_embeddings()

        vectorstore = create_vectorstore(
            chunks,
            embeddings
        )

    st.success(
        "Document processed successfully."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Summary",
            "Chat",
            "Insights"
        ]
    )

    # -------------------------------------------------
    # TAB 1
    # -------------------------------------------------

    with tab1:

        st.subheader(
            "Generate Summary"
        )

        summary_type = st.selectbox(
            "Summary Length",
            [
                "Short",
                "Medium",
                "Detailed"
            ]
        )

        if st.button(
            "Generate Summary"
        ):

            graph = build_summary_graph()

            start = time.time()

            result = graph.invoke(
                {
                    "chunks": [
                        c.page_content
                        for c in chunks
                    ],
                    "summary_type":
                    summary_type
                }
            )

            elapsed = (
                time.time()
                - start
            )

            final_summary = result[
                "final_summary"
            ]

            st.session_state[
                "summary"
            ] = final_summary

            st.session_state[
                "summary_time"
            ] = elapsed

            st.markdown(
                final_summary
            )

            st.info(
                f"Generated in {elapsed:.2f} seconds"
            )

        if "summary" in st.session_state:

            if st.button(
                "Save Summary"
            ):

                file_path = save_summary(
                    st.session_state[
                        "summary"
                    ],
                    "summary.txt"
                )

                st.success(
                    f"Saved: {file_path}"
                )

    # -------------------------------------------------
    # TAB 2
    # -------------------------------------------------

    with tab2:

        st.subheader(
            "Chat With Document"
        )

        question = st.text_input(
            "Ask a question"
        )

        if st.button(
            "Get Answer"
        ):

            with st.spinner(
                "Searching document..."
            ):

                answer, docs = (
                    answer_question(
                        vectorstore,
                        question
                    )
                )

            st.markdown(
                "### Answer"
            )

            st.write(
                answer
            )

            with st.expander(
                "Retrieved Context"
            ):

                for i, doc in enumerate(docs):

                    st.markdown(
                        f"### Chunk {i+1}"
                    )

                    st.write(
                        doc.page_content
                    )

    # -------------------------------------------------
    # TAB 3
    # -------------------------------------------------

    with tab3:

        st.subheader(
            "Document Insights"
        )

        st.metric(
            "Pages",
            len(documents)
        )

        st.metric(
            "Chunks",
            len(chunks)
        )

        st.metric(
            "Model",
            "Llama 3.1 8B"
        )

        if (
            "summary_time"
            in st.session_state
        ):

            st.metric(
                "Summary Time",
                f"{st.session_state['summary_time']:.2f}s"
            )