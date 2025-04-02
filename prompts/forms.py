"""
This module contains the form for creating rubrics.
"""

from django import forms
from django.forms import ModelForm
from .models import Prompt


class PromptForm(ModelForm):
    """
    This form is used to create a prompt.
    """

    class Meta:
        """
        Meta class for PromptForm.
        """

        model = Prompt
        fields = ["name"]
        labels = {"name": "nombre"}

    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "id": "Nombre",
                "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6",
            }
        ),
        required=True,
    )

    prompt = forms.CharField(
        label="Prompt",
        widget=forms.Textarea(
            attrs={
                "id": "prompt",
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "rows": 4,
                "placeholder": "Escribe tu prompt aquí...",
            }
        ),
        required=True,
    )
