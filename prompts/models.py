"""
This file contains the models for the prompts app.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Prompt(models.Model):
    """
    Model representing a prompt.
    """

    name = models.CharField(max_length=150)
    prompt = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts")
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for Prompt model.
        """

        constraints = [
            models.UniqueConstraint(
                fields=("name", "user"), name="unique_prompts_x_user"
            )
        ]

    def __str__(self):
        return self.name
