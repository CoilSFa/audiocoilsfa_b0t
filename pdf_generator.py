from fpdf import FPDF
import datetime
import os

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    
    # Используем встроенный шрифт Helvetica
    pdf.set_font("Helvetica", size=12)

    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)

    filename = f"summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
