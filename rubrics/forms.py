""" Form for registering a Rubric. """
from django import forms
from django.forms import ModelForm
from .models import Rubric


class RubricForm(ModelForm):
    """
    Class to create a form for a new rubric entry in the database.
    """


    class Meta:
        """
        Class to define the fields of the rubrics form.
        """

        model = Rubric
        fields = ["name"]
        labels = {"name": "Nombre"}

    # Specific style attributes for fields.

    rubric_file = forms.FileField(
        label="Archivo Markdown",
        required=True,
        help_text="Sube un archivo Markdown con la rúbrica",
        widget=forms.ClearableFileInput(
            attrs={
                "id": "rubic_file",
                "class": "input-custom",
            }
        ),
    )

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
        Validate the file with the content of the rubric.
        
        Parameters:
            self: The form instance.
            
        Returns:
            str: The content of the file if valid.
            
        Raises:
            forms.ValidationError: If the file is not a Markdown file or if it is not UTF-8 encoded.
        """
        file = self.cleaned_data.get("rubric_file")

        if not file.name.endswith(".md"):
            raise forms.ValidationError("El archivo subido no es un archivo Markdown")

        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError as exc:
            raise forms.ValidationError("El archivo debe estar codificado en UTF-8") from exc

        return content
