from fpdf import FPDF
import datetime

def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Добавляем Unicode-шрифт
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Устанавливаем ширину страницы с учётом отступов
    page_width = pdf.w - 2 * pdf.l_margin

    # Добавляем текст с автоматическим переносом
    pdf.multi_cell(page_width, 10, text)

    filename = f"summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
