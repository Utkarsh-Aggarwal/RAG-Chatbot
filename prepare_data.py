import re

def split_text(text, chunk_size=1500):
    """
    Splits the text into chunks based on paragraphs and ensures that chunks do not exceed the specified size.
    """
    # Split text by paragraphs or sections
    paragraphs = re.split(r'\n\n+', text)
    chunks = []
    chunk = ""
    
    for paragraph in paragraphs:
        # Add paragraph to current chunk
        if len(chunk) + len(paragraph) < chunk_size:
            chunk += paragraph + "\n\n"
        else:
            # Add the current chunk to the list and start a new chunk
            if chunk:
                chunks.append(chunk.strip())
            chunk = paragraph + "\n\n"
    
    # Add the last chunk if it exists
    if chunk:
        chunks.append(chunk.strip())
    
    return chunks

if __name__ == "__main__":
    # Read the extracted text from file
    with open('extracted_text.txt', 'r') as f:
        text = f.read()

    # Split text into chunks
    chunks = split_text(text)

    # Write chunks to file
    with open('document_chunks.txt', 'w') as f:
        for chunk in chunks:
            f.write(chunk + '\n\n')  # Ensure separation between chunks

    print("Data preparation complete.")
