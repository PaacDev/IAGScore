"""
This file contains the tests for the accounts app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm


User = get_user_model()


class CustomUserTests(TestCase):
    """
    This class contains the tests for the custom user model.
    """

    def setUp(self):
        """
        Initial test configuration
        """
        self.superuser = User.objects.create_superuser(
            username="superuser", email="super@mail.com", password="superpass123"
        )

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_create_user(self):
        """
        Testing user creation
        """

        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@mail.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        """
        Testing superuser creation
        """
        self.assertEqual(self.superuser.username, "superuser")
        self.assertEqual(self.superuser.email, "super@mail.com")
        self.assertTrue(self.superuser.check_password("superpass123"))
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)


class RegisterFormTests(TestCase):
    """
    This class contains the tests for the register form.
    """

    def setUp(self):
        """
        Initial test configuration
        """

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )

    def test_register_form_view_page(self):
        response = self.client.get(reverse("register"))

        self.assertEquals(response.status_code, 200)

    def test_valid_register_form(self):
        """
        Testing valid form
        """
        form = RegisterForm(
            data={
                "username": "testuser2",
                "email": "testuser2@mail.com",
                "password": "testpass123",
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser2")
        self.assertEqual(user.email, "testuser2@mail.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)

    def test_invalid_register_form(self):
        """
        Testing invalid form
        """
        form = RegisterForm(data={"username": "", "email": "", "password": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_register_form_exist(self):
        """
        Testing invalid form with existing email
        """
        form = RegisterForm(
            data={
                "username": "testuser",
                "email": self.user.email,
                "password": "test123456",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("User with this Email already exists.", form.errors["email"])

    def test_invalid_register_response(self):
        """
        Testing response with invalid form
        """
        response = self.client.post(
            reverse("register"),
            {
                "username": "newtestuser",
                "email": "testuser@mail.com",
                "password": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newtestuser").exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue("User with this Email already exists" in str(messages_list[0]))

    def test_register_success(self):
        """
        Testing successful registration
        """
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@mail.com",
                "password": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
        self.assertTrue(User.objects.filter(email="newuser@mail.com").exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Usuario creado correctamente")
