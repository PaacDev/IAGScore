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
                "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6",
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
                "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6",
                "placeholder": "Nombre",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6",
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
