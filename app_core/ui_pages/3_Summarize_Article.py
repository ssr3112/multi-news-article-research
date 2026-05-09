import streamlit as st
from app_core.llm.summarizer import summarize_text

st.title("📝 Summarize Selected Article")

if st.session_state.get("metadata") is None:
    st.warning("Please build the article index first from the Input URLs page.")
    st.stop()

metadata = st.session_state.metadata

# Group chunks by URL so each article stays unique
articles = {}

for item in metadata:
    url = item["url"]
    title = item.get("title", "Untitled Article")

    if url not in articles:
        articles[url] = {
            "title": title,
            "chunks": []
        }

    articles[url]["chunks"].append(item["chunk"])


article_options = {
    f"{data['title']}": url for url, data in articles.items()
}

selected_label = st.selectbox(
    "Select an article to summarize",
    options=list(article_options.keys()),
    index=None,
    placeholder="Choose an article"
)

if selected_label:
    selected_url = article_options[selected_label]
    selected_article = articles[selected_url]

    st.write("### Selected Article")
    st.write(f"**Title:** {selected_article['title']}")
    st.write(f"**URL:** {selected_url}")

    if st.button("Summarize Article"):
        full_text = " ".join(selected_article["chunks"])

        with st.spinner("Generating summary..."):
            summary = summarize_text(full_text)

        st.subheader("Article Summary")
        st.write(summary)

        with st.expander("Preview Article Text"):
            st.write(full_text[:3000] + ("..." if len(full_text) > 3000 else ""))