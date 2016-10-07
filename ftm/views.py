from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
import validators

from .analyze import analyze


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
            return render(request, "result/index.html", analyze(form.cleaned_data["domain_name"]))

    return render(request, "index.html", {"form": form})
