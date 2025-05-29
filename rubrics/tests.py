"""
Tests for the rubrics app.
"""

import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import messages
from .models import Rubric
from .forms import RubricForm

User = get_user_model()
# Silence Django 404 logging during tests
logging.getLogger("django.request").setLevel(logging.CRITICAL)


class RubricModelTestCase(TestCase):
    """
    Test case for the Rubric model.
    """

    def setUp(self):
        """
        Set up the test case
        """

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_create_rubric(self):
        """
        Test creating a Rubric
        """

        rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        self.assertEqual(rubric.name, "Test Rubric")
        self.assertEqual(rubric.content, "# This is a test rubric.")
        self.assertEqual(rubric.user, self.user)
        self.assertEqual(str(rubric), "Test Rubric")
        self.assertEqual(rubric.get_html_content(), "<h1>This is a test rubric.</h1>")


class RubricFormTestCase(TestCase):
    """
    Test case for the RubricForm.
    """

    def setUp(self):
        """
        Set up the test case
        """

        text = "# This is a test rubric. ñ"

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        self.md_file = SimpleUploadedFile(
            name="test_rubric.md",
            content=text.encode("utf-8"),
            content_type="text/markdown",
        )

        self.no_md_file = SimpleUploadedFile(
            name="test_rubric.txt",
            content=text.encode("utf-8"),
            content_type="text/plain",
        )

        self.no_utf_file = SimpleUploadedFile(
            name="test_rubric.md",
            content=text.encode("latin-1"),
            content_type="text/Markdown",
        )

    def test_valid_form(self):
        """
        Test a valid RubricForm
        """
        data = {
            "name": "new_rubric",
        }

        file = {
            "rubric_file": self.md_file,
        }

        form = RubricForm(data=data, files=file)
        self.assertTrue(form.is_valid())

    def test_invalid_form_no_md(self):
        """
        Test an invalid RubricForm
        """
        data = {
            "name": self.rubric.name,
        }

        file = {
            "rubric_file": self.no_md_file,
        }

        form = RubricForm(data=data, files=file)
        self.assertFalse(form.is_valid())

    def test_invalid_form_no_utf(self):
        """
        Test an invalid RubricForm
        """
        data = {
            "name": self.rubric.name,
        }

        file = {
            "rubric_file": self.no_utf_file,
        }

        form = RubricForm(data=data, files=file)
        self.assertFalse(form.is_valid())


class RubricViewTestCase(TestCase):
    """
    Test case for the Rubric views.
    """

    def setUp(self):
        """
        Set up the test case
        """
        self.password = "testpass123"
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password=self.password
        )

        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        text = "# This is a test rubric. ñ"

        self.md_file = SimpleUploadedFile(
            name="test_rubric.md",
            content=text.encode("utf-8"),
            content_type="text/markdown",
        )

        self.client.login(username=self.user.email, password=self.password)

    def test_rubric_page_view_get(self):
        """
        Test the rubric page view
        """

        response = self.client.get(reverse("rubrics_page"))
        self.assertEqual(response.status_code, 200)

    def test_rubric_page_view_post(self):
        """
        Test the rubric page view
        """
        response = self.client.post(
            reverse("rubrics_page"),
            {
                "name": "new_rubric",
                "rubric_file": self.md_file,
            },
        )

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages_list[0]), "Rúbrica importada correctamente")
        self.assertTrue(Rubric.objects.filter(name="new_rubric").exists())

    def test_invalid_rubric_page_view_integrity(self):
        """
        Test the rubric page view
        """

        self.assertTrue(Rubric.objects.filter(name=self.rubric.name).exists())

        response = self.client.post(
            reverse("rubrics_page"),
            {
                "name": self.rubric.name,
                "rubric_file": self.md_file,
            },
        )
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(messages_list[0]),
            "Error al guardar la rúbrica: Rubrica ya existente",
        )

    def test_invalid_rubric_page_view(self):
        """
        Test the invalid rubric page view
        """
        response = self.client.post(
            reverse("rubrics_page"),
            {
                "name": "",
                "rubric_file": self.md_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ("Este campo es requerido."))

    def test_show_rubric_view(self):
        """
        Test the show rubric view
        """
        response = self.client.get(reverse("show_rubric", args=[self.rubric.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rubrics/rubric.html")
        self.assertContains(response, self.rubric.get_html_content())
        item_id, _ = self.rubric.delete()
        response = self.client.get(reverse("show_rubric", args=[item_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_rubric_view(self):
        """
        Test the delete rubric view
        """
        response = self.client.post(reverse("delete_rubric", args=[self.rubric.id]))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages_list[0]), "Rúbrica eliminada correctamente")
        self.assertFalse(Rubric.objects.filter(id=self.rubric.id).exists())

    def test_query_filtering(self):
        """
        Test the query filtering in the prompt list
        """
        Rubric.objects.create(
            name="First Test",
            content="# This is a test rubric.",
            user=self.user,
        )
        Rubric.objects.create(
            name="Second test",
            content="# This is a test rubric.",
            user=self.user,
        )
        Rubric.objects.create(
            name="Another one",
            content="# This is a test rubric.",
            user=self.user,
        )
        response = self.client.get(reverse("rubrics_page"), {"q": "First"})
        self.assertContains(response, "First Test")
        self.assertNotContains(response, "Second test")
        self.assertNotContains(response, "Another one")
