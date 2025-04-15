"""
This module contains de Test Cases for a correction app
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from prompts.models import Prompt
from rubrics.models import Rubric
from .forms import CorrectionForm
from .models import Correction

User = get_user_model()


class CorrectioModelTestCase(TestCase):
    """
    Test case for the Correction model
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

    def test_create_correcion(self):
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
        self.assertTrue(correction_list.contains(correction))
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

        # No Prompt
        data = {
            "rubric": self.rubric,
            "description": self.description,
            "llm_model": self.llm_model,
        }
        form = CorrectionForm(data=data, files=file)
        self.assertFalse(form.is_valid())
