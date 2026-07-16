from app.utils.pdf_reader import extract_pdf_text
from app.utils.docx_reader import extract_docx_text
from app.utils.txt_reader import extract_txt_text


def extract_text(file_path: str, extension: str):

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    if extension == ".txt":
        return extract_txt_text(file_path)

    return ""