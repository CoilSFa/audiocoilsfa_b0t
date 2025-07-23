from fpdf import FPDF
import os

def generate_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()

    font_path = "FreeSans.ttf"  # Убедись, что файл есть в рабочей директории

    # Подключаем шрифт с поддержкой Unicode
    if "FreeSans" not in pdf.core_fonts:
        pdf.add_font("FreeSans", "", font_path, uni=True)

    pdf.set_font("FreeSans", size=12)

    # Печатаем по строкам, если текст большой
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename
