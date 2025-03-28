"""
This file contains the tests for the core app.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

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
        response = self.client.post(
            "", {"username": self.user.email, "password": "testpass123"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "testuser")
        self.assertEqual(response.wsgi_request.user.email, "testuser@mail.com")
        self.assertFalse(response.wsgi_request.user.is_staff)
        self.assertFalse(response.wsgi_request.user.is_superuser)

    def test_login_invalid_credentials(self):
        """
        Testing invalid credentials
        """
        response = self.client.post(
            "", {"username": "testuser@mail.com", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Usuario o contraseña incorrectos")
        
    def test_login_get(self):
        """
        Testing get in login page
        """
        response = self.client.get("") 
        
        self.assertEqual(response.status_code, 200)
        
    def test_logout(self):

        response = self.client.post(
            "", {"username": self.user.email, "password": "testpass123"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        self.client.logout()
        new_response = self.client.get(reverse('home'))
        self.assertFalse(new_response.wsgi_request.user.is_authenticated)
        
        response_login = self.client.post(
            "", {"username": self.user.email, "password": "testpass123"}
        )
        self.assertTrue(response_login.wsgi_request.user.is_authenticated)
        response_logout = self.client.get(reverse('logout'))
        self.assertFalse(response_logout.wsgi_request.user.is_authenticated)
        self.assertEqual(response_logout.status_code, 302)

class HomeTests(TestCase):
    
    def setUp(self):
        """
        Initial test configuration
        """

        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )
    
    def test_home(self):
        '''
        Home views test
        '''
        response = self.client.post(
            "", {"username": self.user.email, "password": "testpass123"}
        )
        
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        response_home = self.client.get(reverse('home'))
        self.assertTrue(response_home.status_code, 302)