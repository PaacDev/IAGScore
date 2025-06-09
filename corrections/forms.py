"""Form for registering a Correction."""

from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from .models import Correction

# Choices for the model context length
# (int, str) tuples for the dropdown selection in the form.
MODEL_CONTEXT_CHOICES = [
    (2048, "2048 tokens"),
    (4096, "4096 tokens"),
    (8192, "8192 tokens"),
]


class CorrectionForm(ModelForm):
    """
    Class to create a form for a new correction entry in the database.
    """

    class Meta:
        """
        Class to define the fields of the corrections form.
        """

        model = Correction
        fields = [
            "description",
            "llm_model",
            "rubric",
            "prompt",
            "model_temp",
            "model_top_p",
            "model_top_k",
            "output_format",
            "model_context_length",
        ]
        labels = {
            "description": _("Descripción"),
            "llm_model": _("Modelo usado"),
            "rubric": _("Rúbrica"),
            "prompt": _("Prompt"),
            "model_temp": _("Temperatura"),
            "model_top_p": "Top P",
            "model_top_k": "Top K",
            "output_format": _("Formato de salida"),
            "model_context_length": _("Ventana de contexto del modelo"),
        }

    # Specific style attributes for fields.

    description = forms.CharField(
        label=_("Descripcion"),
        widget=forms.TextInput(
            attrs={
                "id": "description",
                "class": "input-custom",
            }
        ),
        required=True,
    )

    llm_model = forms.CharField(
        label=_("modelo"),
        widget=forms.TextInput(
            attrs={
                "id": "model",
                "class": "input-custom",
            }
        ),
        required=True,
        initial="llama3",
    )

    zip_file = forms.FileField(
        label=_("Archivo ZIP"),
        required=True,
        help_text=_("Formatos permitidos: .zip, .rar, .7z o .tar"),
        widget=forms.ClearableFileInput(
            attrs={
                "id": "zip_file",
                "class": "input-custom",
                "aria-describedby": "zip_file_help",
            }
        ),
    )

    model_temp = forms.FloatField(
        label=_("Temperatura"),
        widget=forms.NumberInput(
            attrs={
                "id": "model_temp",
                "class": "input-custom",
                "step": "0.1",
            }
        ),
        required=False,
        initial=0.8,
        min_value=0.0,
        max_value=1.0,
        help_text=_("Temperatura del modelo (0.0 - 1.0)"),
    )

    model_top_p = forms.FloatField(
        label="Top P",
        widget=forms.NumberInput(
            attrs={
                "id": "model_top_p",
                "class": "input-custom",
                "step": "0.1",
            }
        ),
        required=False,
        initial=0.9,
        min_value=0.0,
        max_value=1.0,
        help_text=_("Top P del modelo (0.0 - 1.0)"),
    )

    model_top_k = forms.IntegerField(
        label="Top K",
        widget=forms.NumberInput(
            attrs={
                "id": "model_top_k",
                "class": "input-custom",
                "step": "1",
            }
        ),
        required=False,
        initial=40,
        min_value=0,
        max_value=100,
        help_text=_("Top K del modelo (0 - 100)"),
    )

    output_format = forms.ChoiceField(
        label=_("Formato de salida"),
        choices=[
            ("", "TXT"),
            ("json", "JSON"),
        ],
        widget=forms.Select(
            attrs={
                "id": "output_format",
                "class": "input-custom",
            }
        ),
        required=False,
        initial="TXT",
    )

    model_context_length = forms.ChoiceField(
        label=_("Ventana de contexto del modelo"),
        choices=MODEL_CONTEXT_CHOICES,
        widget=forms.Select(
            attrs={
                "id": "model_context_length",
                "class": "input-custom",
            }
        ),
        required=False,
        initial=2048,
    )

    def clean_zip_file(self):
        """
        Validate the zip file.

        Parameters:
            self (CorrectionForm): The instance of the form.

        Returns:
            file: The uploaded file if it is a valid ZIP.

        Raises:
            ValidationError: If the uploaded file is not a ZIP.
        """
        file = self.cleaned_data.get("zip_file")
        if not file.name.endswith((".zip", ".rar", ".7z", ".tar")):
            raise forms.ValidationError(
                _(
                    "El archivo subido no es un archivo con extensión .zip, .rar, .7z o .tar."
                )
            )

        return file
