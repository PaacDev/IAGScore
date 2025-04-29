"""
This file contains the test for the prompts app.
"""

import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Prompt

User = get_user_model()
# Silence Django 404 logging during tests
logging.getLogger("corrections.signals").setLevel(logging.CRITICAL)


class PrompModelTest(TestCase):
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


class PromptViewTestCase(TestCase):
    """
    Test case for the PromptForm
    """

    def setUp(self):
        """
        Set up the test case
        """
        self.password = "testpass123"
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password=self.password
        )

        self.name = "TestPrompt"
        self.prompt = "Texto para probar el funcionamiento del prompt form"
        self.client.login(username=self.user.email, password=self.password)

    def test_get_prompt_page(self):
        """
        Test the prompt page
        """
        response = self.client.get(reverse("prompts_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prompts/mis_prompts.html")

    def test_valid_prompt_form(self):
        """
        Test the vaslid propm view
        """
        response = self.client.post(
            reverse("prompts_page"),
            {"name": self.name, "prompt": self.prompt},
        )
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages_list[0]), "Prompt creado correctamente")
        self.assertTrue(Prompt.objects.filter(name=self.name).exists())

    def test_invalid_prompt_integrity(self):
        """
        Test
        """
        self.assertFalse(Prompt.objects.filter(name=self.name).exists())
        Prompt.objects.create(name=self.name, prompt=self.prompt, user=self.user)

        self.assertTrue(Prompt.objects.filter(name=self.name).exists())

        response = self.client.post(
            reverse("prompts_page"),
            {"name": self.name, "prompt": "Otro prompt con el mismo nombre"},
        )
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(messages_list[0]), "Error al guardar el prompt: Prompt ya existente"
        )

    def test_invalid_prompt_form(self):
        """
        Test the invalid prompt form
        """
        response = self.client.post(
            reverse("prompts_page"),
            {"name": "", "prompt": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ("Este campo es requerido."))

    def test_show_prompt_view(self):
        """
        Test the show prompt view
        """
        prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

        response = self.client.get(reverse("show_prompt", args=[prompt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prompts/show_prompt.html")
        self.assertContains(response, prompt.prompt)
        item_id, _ = prompt.delete()
        response = self.client.get(reverse("show_prompt", args=[item_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_prompt_view(self):
        """
        Test the delete prompt view
        """
        prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

        item_id = prompt.id
        response = self.client.get(reverse("delete_prompt", args=[prompt.id]))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages_list[0]), "Prompt eliminado correctamente")
        self.assertFalse(Prompt.objects.filter(id=item_id).exists())
