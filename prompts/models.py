""" Model definition for Prompt. """
from django.db import models
from django.contrib.auth import get_user_model

# Get the active user model
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
        # Define the unique constraint for the name and user fields
        # This ensures that a user cannot have two prompts with the same name
        constraints = [
            models.UniqueConstraint(
                fields=("name", "user"), name="unique_prompts_x_user"
            )
        ]

    def __str__(self):
        """
        Overrides the string representation of the Prompt model.
        
        Parameters:
            self (Prompt): The Prompt instance.
            
        Returns:
            str: The name of the prompt.
        """
        return self.name
