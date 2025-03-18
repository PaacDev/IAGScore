'''
This file is used to create the form for the user registration.
'''
from django import forms
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    '''
    This class is used to create the form for the user registration.
    '''
    class Meta:
        '''
        This class is used to define the fields of the form.
        '''
        model = CustomUser
        fields = ["username", "email", "password"]
        labels = {
            "username": "Nombre",
            "email": "Correo electrónico",
            "password": "Contraseña",
        }

    # Widgwts for the form fields
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
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
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "Nombre",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "********",
            }
        ),
        required=True,
    )


    def save(self, commit=True):
        '''
        Save the user 
        '''
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        # Encrypt the password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
