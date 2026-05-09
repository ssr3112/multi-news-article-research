import streamlit as st

st.title("📰 Multi-Article Research Tool")
st.write("Use the navigation menu to add article URLs, build the index, and ask questions.")

if st.session_state.get("processed_urls"):
    st.subheader("Indexed URLs")
    for url in st.session_state.processed_urls:
        st.write(f"- {url}")
else:
    st.info("No articles indexed yet. Go to 'Input URLs' first.")