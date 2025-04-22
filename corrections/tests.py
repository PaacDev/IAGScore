"""
This module contains de Test Cases for a correction app
"""
import logging
import zipfile
import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from prompts.models import Prompt
from rubrics.models import Rubric
from .forms import CorrectionForm
from .models import Correction

User = get_user_model()
# Silence Django 404 logging during tests
logging.getLogger("django.request").setLevel(logging.CRITICAL)


class CorrectioModelTestCase(TestCase):
    """
    Test case for the Correction model
    """

    def setUp(self):
        """
        Set up the test case
        """
        # User
        self.password = "testpass123"
        
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password=self.password
        )

        # Rubric
        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        # Prompt
        self.prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

    def test_create_correction(self):
        """
        Test creating a Correction
        """
        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Correction Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )

        self.assertEqual(correction.description, "Correction Test")
        self.assertEqual(correction.llm_model, "Modelo")
        self.assertEqual(correction.folder_path, "/media/folder/")
        self.assertEqual(correction.rubric, self.rubric)
        self.assertEqual(correction.prompt, self.prompt)
        self.assertEqual(correction.user, self.user)
        self.assertEqual(str(correction), correction.description)

    def test_delete_correction(self):
        """
        Test deleting a Correction
        """
        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Correction Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )

        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 1)
        self.assertIn(correction, correction_list)
        correction_list.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 0)

    def test_update_correction(self):
        """
        Test deleting a Correction
        """
        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Correction Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )

        self.assertEqual(correction.description, "Correction Test")
        correction.description = "Update Correction Test"
        correction.save()
        self.assertEqual(correction.description, "Update Correction Test")


class CorrectionFormTestCase(TestCase):
    """
    Test case for the CorrectionForm
    """

    def setUp(self):
        """
        Set up the test case
        """
        # User
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

        # Rubric
        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        # Prompt
        self.prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )

        # Zip File Simulate
        self.zip_file = SimpleUploadedFile(
            name="zipfile.zip", content=b"ZIP content", content_type="application/zip"
        )

        # No Zip File Similate
        self.no_zip_file = SimpleUploadedFile(
            name="TextFile.txt",
            content=b"Text",
            content_type="text/plain",
        )

        self.description = "Correction Test Form"
        self.llm_model = "Modelo"
        self.folder_path = "/media/folder"

    def test_valid_form(self):
        """
        Test a valid CorrectionForm
        """
        data = {
            "rubric": self.rubric,
            "prompt": self.prompt,
            "description": self.description,
            "llm_model": self.llm_model,
        }

        file = {"zip_file": self.zip_file}

        form = CorrectionForm(data=data, files=file)
        self.assertTrue(form.is_valid())

    def test_invalid_form_zipfile(self):
        """
        Test a invalid file
        """
        data = {
            "rubric": self.rubric,
            "prompt": self.prompt,
            "description": self.description,
            "llm_model": self.llm_model,
        }

        file = {"zip_file": self.no_zip_file}
        form = CorrectionForm(data=data, files=file)
        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        """
        Test a invalid file
        """
        # No rubric
        data = {
            "prompt": self.prompt,
            "description": self.description,
            "llm_model": self.llm_model,
        }

        file = {"zip_file": self.zip_file}
        form = CorrectionForm(data=data, files=file)
        self.assertFalse(form.is_valid())
        self.assertIn('rubric', form.errors)

        # No Prompt
        data = {
            "rubric": self.rubric,
            "description": self.description,
            "llm_model": self.llm_model,
        }
        form = CorrectionForm(data=data, files=file)
        self.assertFalse(form.is_valid())
        self.assertIn('prompt', form.errors)

class CorrectionsViewsTestCase(TestCase):
    """
    Test case for Correction views
    """
    def setUp(self):
        """
        Set up the test case
        """
        # User
        self.password = "testpass123"
        
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password=self.password
        )
        
        # Crear un archivo ZIP válido en memoria con un fichero .java
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Agregar un archivo .java de ejemplo
            java_content = """
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """
            zip_file.writestr("Test.java", java_content)

        # Mover el puntero al inicio del buffer
        zip_buffer.seek(0)

        # Crear el SimpleUploadedFile con el contenido del ZIP
        self.zip_file = SimpleUploadedFile(
            name="zipfile.zip",
            content=zip_buffer.getvalue(),
            content_type="application/zip"
        )

        # Rubric
        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# This is a test rubric.",
            user=self.user,
        )

        # Prompt
        self.prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="This is a test prompt.",
            user=self.user,
        )
        self.client.login(username=self.user.email, password=self.password)
        
    def test_show_correction_base(self):
        """
        Test the base correction view
        """
        response = self.client.get(reverse("corrections"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'corrections/correction_base.html')

    def test_show_view_correction_view(self):
        """
        Test the show view correction view
        """
        response = self.client.get(reverse("show_view_correction"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'corrections/view_correction.html')

    def test_show_new_correction_view_get(self):
        """
        Test the new correction view
        """
        response = self.client.get(reverse("show_new_correction"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'corrections/new_correction.html')

    def test_show_new_correction_view_post(self):
        """
        Test the new correction view
        """
        
        response = self.client.post(
            reverse("show_new_correction"),
            {
                "action": "save_correction",
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3", 
                "zip_file":self.zip_file,
                },
            follow=True,
            )

        self.assertContains(response, "Correción creada correctamente")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'corrections/view_correction.html')

    def test_show_new_correction_view_get_with_rubric_and_prompt(self):
        """
        Test the new correction view with valid rubric_id and prompt_id
        """
        response = self.client.get(
            reverse("show_new_correction"),
            {"rubric_id": self.rubric.id, "prompt_id": self.prompt.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "corrections/new_correction.html")
        self.assertEqual(response.context["rubric_select"], self.rubric)
        self.assertEqual(response.context["prompt_select"], self.prompt)
        self.assertQuerySetEqual(
            response.context["rubric_list"], Rubric.objects.filter(user=self.user)
        )
        self.assertQuerySetEqual(
            response.context["prompt_list"], Prompt.objects.filter(user=self.user)
        )
        
    def test_show_new_correction_view_post_invalid(self):
        """
        Test the new correction view invalid post
        """
        
        response = self.client.post(
            reverse("show_new_correction"),
            {
                "action": "save_correction",
                "rubric": self.rubric.id,
                "prompt": "",
                "description": "test_correction",
                "llm_model": "llama3", 
                "zip_file":self.zip_file,
                },
            follow=True,
            )
        
        correction_list = Correction.objects.all()
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertContains(response, "Error al crear correción")
        self.assertEqual(response.status_code, 200)

    def test_delete_correction_view(self):
        """
        Test the new correction view
        """

        response = self.client.post(
            reverse("show_new_correction"),
            {
                "action": "save_correction",
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3", 
                "zip_file":self.zip_file,
                },
            follow=True,
            )
        
        correction = Correction.objects.get(description="test_correction")

        response_delete = self.client.post(
            reverse("delete_correction", kwargs={"id": correction.id})
        )
        self.assertFalse(Correction.objects.filter(id=correction.id).exists())
        self.assertEqual(response_delete.status_code, 302)
        self.assertRedirects(response_delete, reverse("show_view_correction"))
        
    def test_delete_correction_view_error(self):
        """
        Test the delete correction invalid
        """
        

        response_delete = self.client.post(
            reverse("delete_correction", kwargs={"id": 1001})
        )
        
        self.assertEqual(response_delete.status_code, 404)
        