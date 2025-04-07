"""
This module contains the models for the corrections app.
"""
from django.db import models
from prompts.models import Prompt
from rubrics.models import Rubric


class Correction(models.Model):
    """
    Model representing a correction for a prompt.
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    correction = models.TextField()
    llm_model = models.CharField(max_length=255)


    def __str__(self):
        return f"Correction for {self.prompt} with score {self.score}"