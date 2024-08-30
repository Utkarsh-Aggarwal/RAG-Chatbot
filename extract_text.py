import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

if __name__ == "__main__":
    pdf_path = r"D:\chatbot\document\Harry-Potter-and-the-Sorcerers-Stone.pdf"  # Use raw string for Windows paths
    pdf_text = extract_text_from_pdf(pdf_path)
    with open('extracted_text.txt', 'w') as f:
        f.write(pdf_text)
    print("Text extraction complete.")

    
