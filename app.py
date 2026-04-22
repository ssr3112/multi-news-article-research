import streamlit as st

st.set_page_config(page_title="Multi-Article Research Tool", layout="wide")

if "index" not in st.session_state:
    st.session_state.index = None
if "metadata" not in st.session_state:
    st.session_state.metadata = None
if "processed_urls" not in st.session_state:
    st.session_state.processed_urls = []

pg = st.navigation([
    st.Page("app_core/ui_pages/home.py", title="Home", icon="🏠"),
    st.Page("app_core/ui_pages/1_Input_URLs.py", title="Input URLs", icon="🔗"),
    st.Page("app_core/ui_pages/2_Ask_Questions.py", title="Ask Questions", icon="💬"),
    st.Page("app_core/ui_pages/3_Summarize_Article.py", title="Summarize Article", icon="📝"),
])

pg.run()