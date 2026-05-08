import streamlit as st
from app_core.pipeline.rag_pipeline import search_articles
from app_core.llm.qa_generator import generate_answer

st.title("💬 Ask Questions")

if st.session_state.get("index") is None or st.session_state.get("metadata") is None:
    st.warning("Please build the article index first from the Input URLs page.")
    st.stop()

question = st.text_input("Ask a question about the indexed articles")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Retrieving relevant sources..."):
        contexts = search_articles(
            query=question,
            index=st.session_state.index,
            metadata=st.session_state.metadata,
            k=3
        )

    if not contexts:
        st.error("No relevant context found.")
        st.stop()

    with st.spinner("Generating answer..."):
        answer = generate_answer(question, contexts)

    st.subheader("Answer")
    st.write(answer)

    col1, col2, col3 = st.columns(3)
    col1.metric("Retrieved Sources", len(contexts))
    col2.metric("Indexed Articles", len(set(item["url"] for item in st.session_state.metadata)))
    col3.metric("Question Length", len(question.split()))

    st.markdown("---")
    st.subheader("Top Matching Sources")

    for i, item in enumerate(contexts, start=1):
        title = item.get("title", "Untitled Article")
        url = item.get("url", "No URL available")
        chunk = item.get("chunk", "")
        score = item.get("score", None)

        expander_title = f"{i}. {title}"
        if score is not None:
            expander_title += f"  |  Score: {score:.4f}"

        with st.expander(expander_title):
            st.write(f"**URL:** {url}")
            st.write("**Retrieved Text:**")
            st.write(chunk[:1500] + ("..." if len(chunk) > 1500 else ""))