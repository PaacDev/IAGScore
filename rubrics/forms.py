"""
This module contains the form for creating rubrics.
"""

from django import forms
from django.forms import ModelForm
from .models import Rubric


class RubricForm(ModelForm):
    """
    Form for creating rubrics.
    """

    rubric_file = forms.FileField(
        label="Archivo Markdown",
        required=True,
        help_text="Sube un archivo Markdown con la rúbrica",
        widget=forms.ClearableFileInput(
            attrs={
                "id": "rubic_file",
                "class": "input-custom",
                "aria-describedby": "rubric_file_help",
            }
        ),
    )

    class Meta:
        """
        Meta class for RubricForm.
        """

        model = Rubric
        fields = ["name"]
        labels = {"name": "nombre"}

    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "id": "Nombre",
                "class": "input-custom",
            }
        ),
        required=True,
    )

    def clean_rubric_file(self):
        """
        Validate the rubric file.
        """
        file = self.cleaned_data.get("rubric_file")

        if not file.name.endswith(".md"):
            raise forms.ValidationError("El archivo subido no es un archivo Markdown")

        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            raise forms.ValidationError("El archivo debe estar codificado en UTF-8")

        return content
