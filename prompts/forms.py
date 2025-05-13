""" Form for registering a Prompt. """
from django import forms
from django.forms import ModelForm
from .models import Prompt


class PromptForm(ModelForm):
    """
    Class to create a form for a new prompt entry in the database.
    """

    class Meta:
        """
        Class to define the fields of the prompt form.
        """

        model = Prompt
        fields = ["name"]
        labels = {"name": "nombre"}

    # Specific style attributes for fields.

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

    prompt = forms.CharField(
        label="Prompt",
        widget=forms.Textarea(
            attrs={
                "id": "prompt",
                "class": "input-custom",
                "rows": 4,
                "placeholder": "Escribe tu prompt aquí...",
            }
        ),
        required=True,
    )
