""" Model definition for Correction. """
from django.db import models
from django.contrib.auth import get_user_model
from rubrics.models import Rubric
from prompts.models import Prompt

# Importing the User model from Django's authentication system
User = get_user_model()

class Correction(models.Model):
    """
    Model representing a correction.
    """

    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="corrections"
        )
    rubric = models.ForeignKey(
        Rubric, on_delete=models.CASCADE, related_name="corrections"
        )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="corrections"
        )
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    llm_model = models.CharField(max_length=255, default="llama3")
    folder_path = models.CharField(max_length=255, blank=True)
    last_ejecution_date = models.DateTimeField(null=True)
    running = models.BooleanField(default=False)
    model_temp = models.FloatField(default=0.8)
    model_top_p = models.FloatField(default=0.9)
    model_top_k = models.IntegerField(default=40)
    output_format = models.CharField(
        max_length=255, default="text", choices=[
            ("json", "json"),
            ("text", ""),
        ]
    )

    def __str__(self):
        """ Returns a string representation of the correction. """
        return self.description
