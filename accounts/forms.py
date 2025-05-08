""" Django form for handling user registration. """

from django import forms
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    """
    Class to create the user registration form
    """

    class Meta:
        """
        Class to define the fields of the user registration form.
        """

        model = CustomUser
        fields = ["username", "email", "password"]
        labels = {
            "username": "Nombre",
            "email": "Correo electrónico",
            "password": "Contraseña",
        }

    #Specific style attributes for fields

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "input-custom",
                "placeholder": "name@company.com",
            }
        ),
        required=True,
    )

    username = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "id": "Nombre",
                "class": "input-custom",
                "placeholder": "Nombre",
            }
        ),
        required=True,
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "input-custom",
                "placeholder": "********",
            }
        ),
        required=True,
    )

    def save(self, commit=True):
        """
        Override the save method to set the username and email fields
        
        Parameters:
            commit (bool): If True, save the user instance to the database.
            self (RegisterForm): The form instance.
            
        Returns:
            user (CustomUser): The saved user instance.
        """
        # Instance of the user
        user = super().save(commit=False)
        # Set the username and email fields
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        # Encrypt the password
        user.set_password(self.cleaned_data["password"])
        # Save the user instance if commit is True
        if commit:
            user.save()
        return user
