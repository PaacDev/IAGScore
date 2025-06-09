"""
Test for the prompts app.
"""

import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.admin.sites import AdminSite
from django.utils.translation import activate
from .models import Prompt
from .admin import PromptAdmin

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
        activate("es")
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
        response = self.client.post(reverse("delete_prompt", args=[prompt.id]))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages_list[0]), "Prompt eliminado correctamente")
        self.assertFalse(Prompt.objects.filter(id=item_id).exists())

    def test_delete_prompt_view_raise(self):
        """
        Test the delete prompt view with a non-existing prompt
        """
        prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

        item_id = prompt.id + 1
        response = self.client.post(reverse("delete_prompt", args=[item_id]))
        self.assertEqual(response.status_code, 404)
        self.assertRaises(Prompt.DoesNotExist, Prompt.objects.get, id=item_id)

    def test_query_filtering(self):
        """
        Test the query filtering in the prompt list
        """

        Prompt.objects.create(
            name="First Test",
            prompt="This is a test prompt.",
            user=self.user,
        )
        Prompt.objects.create(
            name="Second test",
            prompt="This is another test prompt.",
            user=self.user,
        )
        Prompt.objects.create(
            name="Another one",
            prompt="This is yet another test prompt.",
            user=self.user,
        )
        response = self.client.get(reverse("prompts_page"), {"q": "First"})
        self.assertContains(response, "First Test")
        self.assertNotContains(response, "Second test")
        self.assertNotContains(response, "Another one")


class PromptAdminTest(TestCase):
    """
    Test case for the PromptAdmin class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.site = AdminSite()
        self.admin = PromptAdmin(Prompt, self.site)
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_prompt_preview_short_content(self):
        """
        Test the prompt_preview method with content shorter than 50 characters.
        """
        short_content = "C" * 49
        prompt = Prompt.objects.create(
            name="Test", prompt=short_content, user_id=self.user.id
        )
        result = self.admin.prompt_preview(prompt)
        self.assertEqual(result, short_content)

    def test_prompt_preview_long_content(self):
        """
        Test the prompt_preview method with content longer than 50 characters.
        """
        long_content = "A" * 51  # 60 characters
        prompt = Prompt.objects.create(
            name="Test", prompt=long_content, user_id=self.user.id
        )
        result = self.admin.prompt_preview(prompt)
        self.assertEqual(result, "A" * 50 + "...")

    def test_prompt_preview_exact_50(self):
        """
        Test the prompt_preview method with content exactly 50 characters long.
        """
        exact_content = "B" * 50
        prompt = Prompt.objects.create(
            name="Test", prompt=exact_content, user_id=self.user.id
        )
        result = self.admin.prompt_preview(prompt)
        self.assertEqual(result, exact_content)
