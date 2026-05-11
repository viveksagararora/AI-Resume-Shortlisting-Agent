import fitz
from docx import Document


def extract_text_from_pdf(pdf_file):
    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


def extract_text_from_docx(docx_file):
    doc = Document(docx_file)

    text = "\n".join([para.text for para in doc.paragraphs])

    return text