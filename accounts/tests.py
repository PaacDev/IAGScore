from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError


User = get_user_model()


class CustomUserTests(TestCase):

    def setUp(self):
        """
        Initial test configuration
        """
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='super@mail.com',
            password='superpass123'
            )

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpass123'
            )

    def test_create_user(self):
        """
        Testing tuser creation
        """

        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@mail.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        """
        Testing superuser creation
        """
        self.assertEqual(self.superuser.username, 'superuser')
        self.assertEqual(self.superuser.email, 'super@mail.com')
        self.assertTrue(self.superuser.check_password('superpass123'))
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
