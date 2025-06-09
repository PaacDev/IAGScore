"""Tests for the core app."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings

User = get_user_model()


class LoginTests(TestCase):
    """
    This class contains the tests for the login view.
    """

    def setUp(self):
        """
        Initial test configuration
        """

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_login_success(self):
        """
        Testing login
        """
        lang = settings.LANGUAGE_CODE
        response = self.client.post(
            f"/{lang}/",
            {"username": self.user.email, "password": "testpass123"},
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/{settings.LANGUAGE_CODE}/home/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "testuser")
        self.assertEqual(response.wsgi_request.user.email, "testuser@mail.com")
        self.assertFalse(response.wsgi_request.user.is_staff)
        self.assertFalse(response.wsgi_request.user.is_superuser)

    def test_login_invalid_credentials(self):
        """
        Testing invalid credentials
        """
        lang = settings.LANGUAGE_CODE
        response = self.client.post(
            f"/{lang}/",
            {"username": "testuser@mail.com", "password": "wrongpass"},
            follow=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Usuario o contraseña incorrectos")

    def test_login_get(self):
        """
        Testing get in login page
        """
        lang = settings.LANGUAGE_CODE
        response = self.client.get(f"/{lang}/", follow=False)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Testing logout
        """
        lang = settings.LANGUAGE_CODE
        response = self.client.post(
            f"/{lang}/",
            {"username": self.user.email, "password": "testpass123"},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        new_response = self.client.get(reverse("home"))
        self.assertFalse(new_response.wsgi_request.user.is_authenticated)


class HomeTests(TestCase):
    """
    This class contains the tests for the home view.
    """

    def setUp(self):
        """
        Initial test configuration
        """

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_home(self):
        """
        Home views test
        """
        lang = settings.LANGUAGE_CODE
        response = self.client.post(
            f"/{lang}/",
            {"username": self.user.email, "password": "testpass123"},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        home_url = f"/{settings.LANGUAGE_CODE}/home/"
        response_home = self.client.get(home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response_home.status_code, 302)


class TermAndPrivTest(TestCase):
    """
    Test case for the Terms and Privacy views.
    """

    def test_pricacidad(self):
        """
        Test the privacy view
        """
        response = self.client.get(reverse("privacidad"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/privacidad.html")

    def test_terminos(self):
        """
        Test the terminos view
        """
        response = self.client.get(reverse("terminos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/terminos.html")


class LLMViewsTest(TestCase):
    """
    Test case for the LLM views.
    """

    def test_llm(self):
        """
        Test the llm view
        """
        response = self.client.get(reverse("llm_section"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/llm_info.html")
