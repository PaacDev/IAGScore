""" Form for registering a Prompt. """
from django.utils.translation import gettext_lazy as _
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
        labels = {"name": _("nombre")}

    # Specific style attributes for fields.

    name = forms.CharField(
        label=_("Nombre"),
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
                "placeholder": _("Escribe tu prompt aquí..."),
            }
        ),
        required=True,
    )
