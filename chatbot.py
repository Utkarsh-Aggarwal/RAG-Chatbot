import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity

# Load the sentence transformer model for embeddings
model = SentenceTransformer('all-mpnet-base-v2')

# Load a smaller summarization model for better performance
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load document chunks from file
def load_chunks(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

chunks = load_chunks('document_chunks.txt')

def get_top_k_chunks(query, k=5):
    query_embedding = model.encode([query], convert_to_tensor=False)
    embeddings = np.array([model.encode([chunk], convert_to_tensor=False)[0] for chunk in chunks])
    similarities = cosine_similarity(query_embedding, embeddings)
    sorted_indices = np.argsort(similarities[0])[::-1][:k]
    top_chunks = [chunks[i] for i in sorted_indices]
    return top_chunks

def generate_response(query):
    relevant_chunks = get_top_k_chunks(query)
    response_text = " ".join(relevant_chunks[:3])  # Limit to top 3 chunks for summarization
    
    # Debugging: Check the length of the response text
    print(f"Length of response text: {len(response_text)}")
    
    if len(response_text) > 1000:
        st.write("Warning: The retrieved text is too long. Consider revising your query.")
    
    try:
        summary = summarizer(response_text, max_length=150, min_length=50, do_sample=False)
        final_response = summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        final_response = "I couldn't process the response."
    
    return final_response

# Streamlit UI
st.title("PDF-based Chatbot")

user_input = st.text_input("You:", "")

if user_input:
    st.write("Processing your query...")
    response = generate_response(user_input)
    st.write("Bot:", response)

    # Debug information
    st.write("Debug Info: Relevant chunks retrieved:", get_top_k_chunks(user_input))
