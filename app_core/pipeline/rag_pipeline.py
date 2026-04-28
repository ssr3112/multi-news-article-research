from app_core.ingestion.article_fetcher import fetch_article_text
from app_core.preprocessing.chunker import chunk_text
from app_core.embeddings.embedding_model import embed_texts
from app_core.embeddings.vector_store import create_faiss_index

from app_core.retriever.retrieval import retrieve_top_k

def build_article_index(urls):
    all_chunks = []

    for url in urls:
        article = fetch_article_text(url)

        if article:
            chunks = chunk_text(article["text"])

            for chunk in chunks:
                all_chunks.append({
                    "title": article["title"],
                    "url": article["url"],
                    "chunk": chunk
                })

    if not all_chunks:
        return None, None

    chunk_texts = [item["chunk"] for item in all_chunks]
    embeddings = embed_texts(chunk_texts)
    index = create_faiss_index(embeddings)

    return index, all_chunks

def search_articles(query, index, metadata, k=3):
    return retrieve_top_k(query, index, metadata, k=k)