"""
This file defines the models for the rubrics app
"""

from django.db import models
from django.contrib.auth import get_user_model
import markdown

# Get the active user model
User = get_user_model()


class Rubric(models.Model):
    """
    Model representing a rubric.
    """

    name = models.CharField(max_length=150)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rubrics")

    class Meta:
        """
        Meta class for Rubric model.
        """

        constraints = [
            models.UniqueConstraint(
                fields=("name", "user"), name="unique_rubrics_x_user"
            )
        ]

    def __str__(self):
        return self.name

    def get_html_content(self):
        """
        Returns the HTML content of the rubric.
        """
        html_content = markdown.markdown(self.content, extensions=["tables"])

        styled_html = f"""
        <div class="rubric-style">
            <style>
                .rubric-style table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                .rubric-style td, .rubric-style th {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;
                }}
                .rubric-style h1 {{
                    color: #333;
                    font-size: 2em;
                    font-family: Arial, sans-serif;
                }}
            </style>
            {html_content}
        </div>
        """
        return styled_html
