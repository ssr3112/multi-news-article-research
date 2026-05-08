import streamlit as st
from app_core.pipeline.rag_pipeline import build_article_index

st.title("🔗 Input Article URLs")

url1 = st.text_input("Article URL 1")
url2 = st.text_input("Article URL 2")
url3 = st.text_input("Article URL 3")

urls = [u.strip() for u in [url1, url2, url3] if u.strip()]

if st.button("Fetch and Build Index"):
    if not urls:
        st.warning("Please enter at least one article URL.")
    else:
        with st.spinner("Fetching articles and building index..."):
            index, metadata = build_article_index(urls)

        if index is not None and metadata is not None:
            st.session_state.index = index
            st.session_state.metadata = metadata
            st.session_state.processed_urls = urls
            st.success(f"Indexed {len(metadata)} chunks from {len(urls)} article(s).")
        else:
            st.error("Failed to build index. Try different article URLs.")