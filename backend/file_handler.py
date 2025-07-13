import fitz  # PyMuPDF

def extract_text(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)
    elif filename.endswith(".txt"):
        return extract_txt_text(file)
    else:
        raise ValueError("Unsupported file type. Only PDF or TXT are allowed.")

def extract_pdf_text(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in pdf])
    pdf.close()
    return text

def extract_txt_text(file):
    return file.read().decode("utf-8")
