from fpdf import FPDF
import uuid
import os

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Добавляем шрифт, поддерживающий кириллицу
    font_path = "FreeSans.ttf"
    if not os.path.isfile(font_path):
        raise Exception("Файл шрифта 'FreeSans.ttf' не найден. Помести его в корень проекта.")

    pdf.add_font("FreeSans", "", font_path, uni=True)
    pdf.set_font("FreeSans", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = f"summary_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    return filename
