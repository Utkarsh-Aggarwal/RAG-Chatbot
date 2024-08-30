from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def create_index(chunks, index_file='faiss_index.index', embeddings_file='embeddings.npy', batch_size=1000):
    # Load the SentenceTransformer model
    model = SentenceTransformer('all-mpnet-base-v2')  # Ensure the same model is used throughout

    # Generate embeddings in batches
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = model.encode(batch_chunks, convert_to_tensor=False)
        all_embeddings.append(batch_embeddings)
    
    embeddings = np.vstack(all_embeddings)
    
    # Save embeddings to file for later use
    np.save(embeddings_file, embeddings)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the index
    faiss.write_index(index, index_file)
    print(f"Index creation complete. Saved to {index_file}")

if __name__ == "__main__":
    with open('document_chunks.txt', 'r') as f:
        chunks = f.read().splitlines()

    create_index(chunks)
