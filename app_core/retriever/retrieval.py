from app_core.embeddings.embedding_model import embed_texts

def retrieve_top_k(query, index, metadata, k=3):
    query_embedding = embed_texts([query])
    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx != -1:
            results.append(metadata[idx])

    return results