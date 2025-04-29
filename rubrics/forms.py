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
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                         "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                         "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
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
        except UnicodeDecodeError as exc:
            raise forms.ValidationError("El archivo debe estar codificado en UTF-8") from exc

        return content
