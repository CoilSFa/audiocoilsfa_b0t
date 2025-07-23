from fpdf import FPDF
import uuid
import os

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
    pdf.set_font('FreeSans', size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = f"summary_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    return filename
