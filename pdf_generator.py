from fpdf import FPDF

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    filename = "summary.pdf"
    pdf.output(filename)
    return filename
