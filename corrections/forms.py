"""
This module contains a form for a Correction model
"""

from django import forms
from django.forms import ModelForm
from .models import Correction


class CorrectionForm(ModelForm):
    """
    Form for creating corrections.
    """

    class Meta:
        """
        Meta class for CorrectionForm.
        """

        model = Correction
        fields = ["description", "llm_model", "rubric", "prompt"]
        labels = {
            "description": "Descripción",
            "llm_model": "Modelo usado",
            "rubric": "Rúbrica",
            "prompt": "Prompt",
        }

    description = forms.CharField(
        label="descripcion",
        widget=forms.TextInput(
            attrs={
                "id": "Descipcion",
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                          "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                          "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
            }
        ),
        required=True,
    )

    llm_model = forms.CharField(
        label="modelo",
        widget=forms.TextInput(
            attrs={
                "id": "Modelo",
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                          "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                          "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
            }
        ),
        required=True,
    )

    zip_file = forms.FileField(
        label="Archivo ZIP",
        required=True,
        help_text="Sube un archivo ZIP con las tareas",
        widget=forms.ClearableFileInput(
            attrs={
                "id": "zip_file",
                "class": "input-custom",
                "aria-describedby": "zip_file_help",
            }
        ),
    )

    def clean_zip_file(self):
        """
        Validate the zip file.
        """
        file = self.cleaned_data.get("zip_file")
        if not file.name.endswith(".zip"):
            raise forms.ValidationError("El archivo subido no es un archivo ZIP")

        return file
