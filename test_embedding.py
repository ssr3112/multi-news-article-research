from app_core.embeddings.embedding_model import embed_texts

texts = [
    "This is the first news article chunk.",
    "This is the second article chunk."
]

embeddings = embed_texts(texts)

print("Shape:", embeddings.shape)
print("First vector preview:", embeddings[0][:10])