from fpdf import FPDF
import datetime

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Добавляем встроенный шрифт DejaVu, поддерживающий Unicode
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Добавляем текст
    lines = text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)

    filename = f"summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
