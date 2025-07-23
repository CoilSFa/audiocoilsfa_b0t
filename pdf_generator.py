from fpdf import FPDF
import uuid

def generate_pdf(summary: str, full_text: str) -> str:
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.add_page()

    pdf.multi_cell(0, 10, "📝 Краткое содержание:\n", ln=True)
    pdf.multi_cell(0, 10, summary + "\n\n")

    pdf.multi_cell(0, 10, "📜 Полная расшифровка:\n", ln=True)
    pdf.multi_cell(0, 10, full_text)

    filename = f"transcript_summary_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    return filename
