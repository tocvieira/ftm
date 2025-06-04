from django.template.loader import render_to_string
from weasyprint import HTML


def generate_pdf(context):
    html_string = render_to_string('result/index.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf
