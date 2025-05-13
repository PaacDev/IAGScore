"""Form for registering a Correction."""
from django import forms
from django.forms import ModelForm
from .models import Correction


class CorrectionForm(ModelForm):
    """
    Class to create a form for a new correction entry in the database.
    """

    class Meta:
        """
        Class to define the fields of the corrections form.
        """

        model = Correction
        fields = ["description", "llm_model", "rubric", "prompt", "model_temp", "model_top_p", "model_top_k", "output_format"]
        labels = {
            "description": "Descripción",
            "llm_model": "Modelo usado",
            "rubric": "Rúbrica",
            "prompt": "Prompt",
            "model_temp": "Temperatura",
            "model_top_p": "Top P",
            "model_top_k": "Top K",
            "output_format": "Formato de salida",
        }

    # Specific style attributes for fields.

    description = forms.CharField(
        label="Descripcion",
        widget=forms.TextInput(
            attrs={
                "id": "description",
                "class": "input-custom",
            }
        ),
        required=True,
    )

    llm_model = forms.CharField(
        label="modelo",
        widget=forms.TextInput(
            attrs={
                "id": "model",
                "class": "input-custom",
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
                "class": "input-custom",
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
                "class": "input-custom",
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
                "class": "input-custom",
            }
        ),
        required=False,
        initial=40,
        min_value=0,
        max_value=100,
        help_text="Top K del modelo (0 - 100)",
    )
    
    output_format = forms.ChoiceField(
        label="Formato de salida",
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
        if not file.name.endswith(".zip"):
            raise forms.ValidationError("El archivo subido no es un archivo ZIP")

        return file
