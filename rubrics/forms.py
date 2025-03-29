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
        required=True,
        help_text="Sube un archivo MarkDown con la rúbrica"
        )

    class Meta:
        """
        Meta class for RubricForm.
        """

        model = Rubric
        fields = ['name']
        labels = {
            'name': 'nombre'
        }
