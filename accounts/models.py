from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):

    email = models.EmailField(max_length=150, unique=True)

    # identifying field
    USERNAME_FIELD = 'email'

    # list of the field names that will be prompted for when creating a
    # user via the createsuperuser management command
    REQUIRED_FIELDS = ['username']
