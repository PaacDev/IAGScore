"""
This module contains the models for the corrections app.
"""
from django.db import models
from prompts.models import Prompt
from rubrics.models import Rubric
from django.contrib.auth import get_user_model

User = get_user_model()


class Correction(models.Model):
    """
    Model representing a correction.
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="corrections")
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, related_name="corrections")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="corrections")
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    llm_model = models.CharField(max_length=255) # Respuesta del modelo
    folder_path = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.description