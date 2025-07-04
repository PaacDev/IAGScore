"""
This module contains de Test Cases for a correction app
"""

import logging
import os
import shutil
import uuid
import zipfile
import io
from unittest.mock import MagicMock, patch
from django.test import TestCase, TransactionTestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import timezone
from corrections.tasks import set_tasks_dict
from iagscore import settings
from prompts.models import Prompt
from rubrics.models import Rubric
from .tasks import start_llm_evaluation
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
        correction.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 0)

    def test_delete_prompt_and_correction(self):
        """
        Test if delete prompt deleting a correction
        """

        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Correction Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )

        prompt_2 = Prompt.objects.create(
            name="Test Prompt 2",
            prompt="This is a test prompt.",
            user=self.user,
        )

        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 1)
        self.assertIn(correction, correction_list)
        prompt_2.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 1)
        self.prompt.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 0)

    def test_delete_rubric_and_correction(self):
        """
        Test if delete rubric deleting a correction
        """

        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Correction Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )
        rubric_2 = Rubric.objects.create(
            name="Test Rubric 2",
            content="# This is a test rubric.",
            user=self.user,
        )

        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 1)
        self.assertIn(correction, correction_list)
        rubric_2.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 1)
        self.rubric.delete()
        correction_list = Correction.objects.filter(user=self.user)
        self.assertEqual(len(correction_list), 0)

    def test_delete_user_and_correction(self):
        """
        Test if delete user deleting a correction
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
        self.user.delete()
        correction_list = Correction.objects.all()
        self.assertEqual(len(correction_list), 0)


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

    def test_valid_form_default_fields(self):
        """
        Test a valid CorrectionForm with default fields
        """
        data = {
            "rubric": self.rubric,
            "prompt": self.prompt,
            "description": self.description,
            "llm_model": self.llm_model,
        }

        file = {"zip_file": self.zip_file}

        form = CorrectionForm(data=data, files=file)
        correction = form.save(commit=False)
        correction.user = self.user
        correction.save()

        self.assertTrue(correction.model_temp, 0.8)
        self.assertTrue(correction.model_top_p, 0.9)
        self.assertTrue(correction.model_top_k, 40)
        self.assertTrue(correction.output_format, "")

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
        self.assertIn("rubric", form.errors)

        # No Prompt
        data = {
            "rubric": self.rubric,
            "description": self.description,
            "llm_model": self.llm_model,
        }
        form = CorrectionForm(data=data, files=file)
        self.assertFalse(form.is_valid())
        self.assertIn("prompt", form.errors)


class CorrectionsViewsTestCase(TransactionTestCase):
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

        # Creating a valid ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add .java
            java_content = """
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """
            zip_file.writestr("Test.java", java_content)

        # Move pointer to the start of the buffer
        zip_buffer.seek(0)

        # Create the SimpleUploadedFile with the ZIP contain
        self.zip_file = SimpleUploadedFile(
            name="zipfile.zip",
            content=zip_buffer.getvalue(),
            content_type="application/zip",
        )

        # Rubric
        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# Only 'pass' or 'fail'",
            user=self.user,
        )

        # Prompt
        self.prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="'Pass' or 'Fail'.",
            user=self.user,
        )
        self.client.login(username=self.user.email, password=self.password)

    def tearDown(self):
        """
        Limpia después de cada prueba eliminando todos los objetos Correction, Rubric, Prompt y User.
        También elimina cualquier archivo almacenado en folder_path.
        """
        Correction.objects.all().delete()

    def test_show_correction_base(self):
        """
        Test the base correction view
        """
        response = self.client.get(reverse("corrections"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "corrections/correction_base.html")

    def test_show_view_correction_view(self):
        """
        Test the show view correction view
        """
        response = self.client.get(reverse("show_view_correction"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "corrections/view_correction.html")

    @patch("corrections.views.ollama.list")
    def test_show_new_correction_view_get(self, mock_ollama_list):
        """
        Test the new correction view
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }
        response = self.client.get(reverse("show_new_correction"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "corrections/new_correction.html")

    @patch("corrections.views.ollama.list")
    def test_show_new_correction_view_post(self, mock_ollama_list):
        """
        Test the new correction view
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }

        response = self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )

        self.assertContains(response, "Corrección creada correctamente")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "corrections/view_correction.html")

    @patch("corrections.views.ollama.list")
    def test_show_new_correction_view_get_with_rubric_and_prompt(
        self, mock_ollama_list
    ):
        """
        Test the new correction view with valid rubric_id and prompt_id
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }
        response = self.client.get(
            reverse("show_new_correction"),
            {"rubric_id": self.rubric.id, "prompt_id": self.prompt.id},
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

    @patch("corrections.views.ollama.list")
    def test_show_new_correction_view_post_invalid(self, mock_ollama_list):
        """
        Test the new correction view invalid post
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }

        response = self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": "",
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )

        self.assertContains(response, "Error al crear correción")
        self.assertEqual(response.status_code, 200)

    @patch("corrections.views.ollama.list")
    def test_delete_correction_view(self, mock_ollama_list):
        """
        Test the new correction view
        """

        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }

        self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )

        correction = Correction.objects.get(description="test_correction")

        response_delete = self.client.post(
            reverse("delete_correction", kwargs={"item_id": correction.id})
        )
        self.assertFalse(Correction.objects.filter(id=correction.id).exists())
        self.assertEqual(response_delete.status_code, 302)
        self.assertRedirects(response_delete, reverse("show_view_correction"))

    @patch("corrections.views.ollama.list")
    def test_delete_correction_view_error(self, mock_ollama_list):
        """
        Test the delete correction invalid
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }

        response_delete = self.client.post(
            reverse("delete_correction", kwargs={"item_id": 1001})
        )

        self.assertEqual(response_delete.status_code, 404)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch("corrections.views.ollama.list")
    @patch("corrections.tasks.OllamaLLM")
    def test_run_model_and_download(self, mock_ollama_class, mock_ollama_list_view):
        """
        Test tdownload the response
        """
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = "simulate model response"
        mock_ollama_class.return_value = mock_llm_instance

        # Mocking the Ollama list to simulate list of models
        mock_ollama_list_view.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }

        response = self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )

        correction = Correction.objects.get(description="test_correction")

        response = self.client.get(
            reverse("run_model", kwargs={"correction_id": correction.id})
        )
        self.assertRedirects(response, reverse("show_view_correction"))

        # Rewrite the response file
        response = self.client.get(
            reverse("run_model", kwargs={"correction_id": correction.id})
        )
        self.assertRedirects(response, reverse("show_view_correction"))

        response_file_path = os.path.join(
            settings.MEDIA_ROOT, correction.folder_path, "response", "response.txt"
        )
        print(f"Checking file path: {response_file_path}")
        print(
            f"Directory exists: {os.path.exists(os.path.dirname(response_file_path))}"
        )
        self.assertTrue(os.path.exists(response_file_path))
        url = reverse("download_response", kwargs={"correction_id": correction.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(
            response["Content-Disposition"], 'attachment; filename="response.txt"'
        )

    def test_run_model_error(self):
        """
        Test tdownload the response
        """

        response = self.client.get(reverse("run_model", kwargs={"correction_id": 1001}))

        self.assertEqual(response.status_code, 404)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch("corrections.tasks.Correction.objects.get")
    def test_start_llm_evaluation_correction_does_not_exist(self, mock_get):
        """
        Simula que la corrección no existe al ejecutar la tarea.
        """
        mock_get.side_effect = Correction.DoesNotExist
        with self.assertRaises(Correction.DoesNotExist):
            start_llm_evaluation(correction_id=9999)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch("corrections.tasks.OllamaLLM")
    @patch("corrections.views.ollama.list")
    def test_start_llm_evaluation_generic_exception(
        self, mock_ollama_list, mock_ollama_class
    ):
        """
        Simula una excepción genérica al ejecutar el modelo.
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }
        self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )
        correction = Correction.objects.get(description="test_correction")
        # Configurar el mock para lanzar una excepción en .invoke()
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.side_effect = Exception("Modelo falló")
        mock_ollama_class.return_value = mock_llm_instance

        with self.assertRaises(Exception) as cm:
            start_llm_evaluation(correction.id)

        self.assertIn("Modelo falló", str(cm.exception))

        # Verifica que se haya marcado como no-running
        correction.refresh_from_db()
        self.assertFalse(correction.running)

    @patch("corrections.views.ollama.list")
    def test_download_response_error(self, mock_ollama_list):
        """
        Test the download response error
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }
        self.client.post(
            reverse("show_new_correction"),
            {
                "rubric": self.rubric.id,
                "prompt": self.prompt.id,
                "description": "test_correction",
                "llm_model": "llama3",
                "zip_file": self.zip_file,
            },
            follow=True,
        )
        response = self.client.get(
            reverse("download_response", kwargs={"correction_id": 1001})
        )

        self.assertEqual(response.status_code, 404)
        correction = Correction.objects.get(description="test_correction")
        response = self.client.get(
            reverse("download_response", kwargs={"correction_id": correction.id})
        )
        self.assertEqual(response.status_code, 404)

    @patch("os.listdir", side_effect=FileNotFoundError)
    def test_set_tasks_dict_folder_not_found(self, mock_listdir):
        """
        Test set_tasks_dict when the folder does nclearot exist
        """
        result = set_tasks_dict("nonexistent_folder")
        self.assertEqual(result, {})

    @patch("os.listdir", side_effect=PermissionError)
    def test_set_tasks_dict_permission_denied(self, mock_listdir):
        """
        Test set_tasks_dict when there is a permission error
        """
        result = set_tasks_dict("restricted_folder")
        self.assertEqual(result, {})

    def test_query_filtering(self):
        """
        Test the query filtering in the correction list
        """
        # Create corrections
        Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="First Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )
        Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Second Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )
        Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Another Test",
            llm_model="Modelo",
            folder_path="/media/folder/",
        )
        response = self.client.get(reverse("show_view_correction"), {"q": "First"})
        self.assertContains(response, "First Test")
        self.assertNotContains(response, "Second test")
        self.assertNotContains(response, "Another one")

    def test_sorting_excludes_null_last_execution_dates(self):
        """
        Test that sorting by last_ejecution_date excludes corrections with null dates.
        """
        # Corrections con y sin fecha de ejecución
        Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="With date",
            llm_model="Modelo",
            folder_path="/media/folder/",
            last_ejecution_date=timezone.now(),
        )

        Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Without date",
            llm_model="Modelo",
            folder_path="/media/folder/",
            last_ejecution_date=None,
        )

        response = self.client.get(
            reverse("show_view_correction") + "?sort=last_ejecution_date"
        )

        # Comprobaciones
        content = response.content.decode()
        self.assertIn("With date", content)
        self.assertNotIn("Without date", content)

    @patch("corrections.views.ollama.list")
    def test_correction_clone(self, mock_ollama_list):
        """
        Test the correction_clone view correctly clones data and redirects.
        """
        # Mocking the Ollama list to simulate list of models
        mock_ollama_list.return_value = {
            "models": [
                {"model": "llama3"},
                {"model": "mistral"},
            ]
        }
        # Crear una instancia de Correction
        correction = Correction.objects.create(
            user=self.user,
            description="Original Correction",
            llm_model="llama3",
            model_temp=0.7,
            model_top_p=0.9,
            model_top_k=40,
            output_format="text",
            rubric=self.rubric,
            prompt=self.prompt,
            folder_path="fake_path",
        )

        # Simular la solicitud de clonación
        response = self.client.get(reverse("correction_clone", args=[correction.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("show_new_correction"))

        # Verificar que el mensaje se agregó
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Datos clonados de la corrección" in m.message for m in messages)
        )

    def test_show_tasks_view_success_and_errors(self):
        """
        Test show_tasks view with valid and invalid cases.
        """
        # Temporal folder for tasks
        folder_relative_path = f"test_correction_{uuid.uuid4().hex}"
        base_path = os.path.join(settings.MEDIA_ROOT, folder_relative_path)
        tasks_path = base_path
        os.makedirs(tasks_path)

        # Simulate valid and invalid task files
        valid_file = "valid_task.java"
        invalid_file = "_hidden.java"
        with open(os.path.join(tasks_path, valid_file), "w") as f:
            f.write("// valid task")
        with open(os.path.join(tasks_path, invalid_file), "w") as f:
            f.write("// invalid task")

        # correction instance
        correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="Test correction with tasks",
            llm_model="llama3",
            folder_path=folder_relative_path,
        )

        with patch("corrections.views.VALID_EXTENSION", ".java"):
            response = self.client.get(
                reverse("show_tasks", kwargs={"item_id": correction.id})
            )

        # Response checks
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, valid_file)
        self.assertNotContains(response, invalid_file)

        # Raise an error correction does not exist
        response = self.client.get(reverse("show_tasks", kwargs={"item_id": 9999}))
        self.assertEqual(response.status_code, 404)
        # Raise an error if the folder does not exist
        with patch("os.path.exists", return_value=False):
            response = self.client.get(
                reverse("show_tasks", kwargs={"item_id": correction.id})
            )
            self.assertEqual(response.status_code, 404)

        # Remove all files in the tasks folder
        for file in os.listdir(tasks_path):
            os.remove(os.path.join(tasks_path, file))
        # Crear solo archivos inválidos
        invalid_file = "_ignored_task.java"
        with open(os.path.join(tasks_path, invalid_file), "w") as f:
            f.write("// this should not be counted")

        response = self.client.get(
            reverse("show_tasks", kwargs={"item_id": correction.id})
        )
        self.assertEqual(response.status_code, 404)

        # Clean up the temporary folder
        shutil.rmtree(base_path)


class DeleteCorrectionFolderTests(TestCase):
    """
    Test case for the deletion of the correction folder
    """

    def setUp(self):
        """
        Set up the test case
        """
        # Crea una instancia falsa de Correction
        self.password = "testpass123"

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password=self.password
        )
        # Rubric
        self.rubric = Rubric.objects.create(
            name="Test Rubric",
            content="# Only 'pass' or 'fail'",
            user=self.user,
        )

        # Prompt
        self.prompt = Prompt.objects.create(
            name="Test Prompt",
            prompt="'Pass' or 'Fail'.",
            user=self.user,
        )
        self.client.login(username=self.user.email, password=self.password)
        self.correction = Correction.objects.create(
            prompt=self.prompt,
            rubric=self.rubric,
            user=self.user,
            description="With date",
            llm_model="Modelo",
            folder_path="/media/folder/",
            last_ejecution_date=timezone.now(),
        )

        self.folder_path = os.path.join(
            settings.MEDIA_ROOT, self.correction.folder_path
        )

    @patch("corrections.signals.os.path.exists", return_value=True)
    @patch("corrections.signals.os.path.isdir", return_value=True)
    @patch("corrections.signals.shutil.rmtree", side_effect=OSError("Permiso denegado"))
    @patch("corrections.signals.logger")
    def test_folder_deletion_error_logged(
        self, mock_logger, mock_rmtree, mock_isdir, mock_exists
    ):
        """
        Test that an error is logged when folder deletion fails
        """
        # Simula la eliminación de la carpeta
        self.correction.delete()

        # Verifica que shutil.rmtree fue llamado con la ruta correcta
        mock_rmtree.assert_called_once_with(self.folder_path)

        # Verifica que se registró un error
        mock_logger.error.assert_called_once()
        self.assertIn("Error al eliminar la carpeta", mock_logger.error.call_args[0][0])
