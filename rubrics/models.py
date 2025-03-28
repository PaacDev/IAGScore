'''
This file defines the models for the rubrics app
'''
from django.db import models
from django.contrib.auth import get_user_model

# Get the active user model
User = get_user_model()


# Create your models here.
class Rubric(models.Model):
    """
    Model representing a rubric.
    """
    
    name = models.CharField(max_length=150)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rubrics')
    
    class Meta:
        """
        Meta class for Rubric model.
        """

        constraints = [
            models.UniqueConstraint(fields=('name','user'), name='unique_rubrics_x_user')
        ]
