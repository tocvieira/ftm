from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
import validators

from .analyze import analyze
from .pdf import generate_pdf


def domain_validator(value):
    if not validators.domain(value):
        raise ValidationError("A sintax do domínio informado é inválida")


class MainForm(forms.Form):
    domain_name = forms.CharField(label="Dominio Analisado", validators=[domain_validator])


def index(request):
    form = MainForm()
    if request.method == "POST":
        form = MainForm(request.POST)
        if form.is_valid():
            context = analyze(form.cleaned_data["domain_name"])
            if request.GET.get("format") == "pdf":
                pdf = generate_pdf(context)
                response = HttpResponse(pdf, content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                return response
            return render(request, "result/index.html", context)

    return render(request, "index.html", {"form": form})
