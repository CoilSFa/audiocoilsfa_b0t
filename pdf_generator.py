from fpdf import FPDF

def generate_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf = FPDF()
    pdf.add_font("FreeSans", "", "FreeSans.ttf", uni=True)
    pdf.set_font("FreeSans", size=12)
    pdf.add_page()

    # Разбиваем текст по строкам, чтобы не выходил за границы страницы
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(filename)
    return filename
