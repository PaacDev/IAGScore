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
        initial="llama3"
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
    
    model_temp = forms.FloatField(
        label="Temperatura",
        widget=forms.TextInput(
            attrs={
                "id": "model_temp",
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                          "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                          "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
            }
        ),
        required=False,
        initial=0.8,
        min_value=0.0,
        max_value=1.0,
        help_text="Temperatura del modelo (0.0 - 1.0)",
    )
    
    model_top_p = forms.FloatField(
        label="Top P",
        widget=forms.TextInput(
            attrs={
                "id": "model_top_p",
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                          "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                          "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
            }
        ),
        required=False,
        initial=0.9,
        min_value=0.0,
        max_value=1.0,
        help_text="Top P del modelo (0.0 - 1.0)",
    )
    
    model_top_k = forms.IntegerField(
        label="Top K",
        widget=forms.TextInput(
            attrs={
                "id": "model_top_k",
                "class": ("block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 "
                          "-outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 "
                          "focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6"),
            }
        ),
        required=False,
        initial=40,
        min_value=0,
        max_value=100,
        help_text="Top K del modelo (0 - 100)",
    )

    def clean_zip_file(self):
        """
        Validate the zip file.
        """
        file = self.cleaned_data.get("zip_file")
        if not file.name.endswith(".zip"):
            raise forms.ValidationError("El archivo subido no es un archivo ZIP")

        return file
