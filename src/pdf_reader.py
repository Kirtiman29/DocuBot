from PyPDF2 import PdfReader

file_path = "data/documents/notes.pdf"

def read_pdf(file_path):
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + " "

    return full_text
