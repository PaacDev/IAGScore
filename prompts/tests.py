"""
This file contains the test for the prompts app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Prompt

User = get_user_model()


class PrompTest(TestCase):
    """
    Test case for the Prompt model.
    """

    def setUp(self):
        """
        Set up the test case
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_create_prompt(self):
        """
        Test creating a Prompt
        """
        prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

        self.assertEqual(prompt.name, "Test Prompt")
        self.assertEqual(prompt.prompt, "This is a test prompt.")
        self.assertEqual(prompt.user, self.user)
        self.assertEqual(str(prompt), "Test Prompt")

    def test_delete_prompt(self):
        """
        Test deleting a Prompt
        """
        prompt = Prompt.objects.create(
            name="Test Prompt 1",
            prompt="This is a test prompt.",
            user=self.user,
        )
        promt_list = Prompt.objects.filter(user=self.user)
        self.assertEqual(len(promt_list), 1)
        prompt.delete()
        promt_list = Prompt.objects.filter(user=self.user)
        self.assertEqual(len(promt_list), 0)
