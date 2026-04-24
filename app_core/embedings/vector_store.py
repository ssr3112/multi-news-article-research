import faiss
import pickle
import os

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_index(index, metadata, file_path):
    with open(file_path, "wb") as f:
        pickle.dump({"index": index, "metadata": metadata}, f)

def load_index(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data