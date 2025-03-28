"""
This file contains the views for the accounts app.
"""
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_GET, require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
import markdown


@require_http_methods(['POST', 'GET'])
@csrf_protect
def custom_login(request):
    """
    This view is used to log in the user.
    - GET: Displays the login form.
    - POST: Processes the form and login.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("home")
        else:
            messages.add_message(
                request, messages.ERROR, "Usuario o contraseña incorrectos"
            )
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

@require_GET
def logout_view(request):
    '''
    Logout
    '''
    logout(request)
    return redirect("login")

@require_GET
@login_required
def home(request):
    """
    This view is used to display the home page
    """
    return render(request, "core/home.html")

@require_safe
def terminos(request):
    """
    This view is used to display the terms and conditions page
    """
    # Path md terminos
    md_terminos = os.path.join(
        settings.STATICFILES_DIRS[2], "core/docs", "terminos.md"
        )

    # Open the file and save its content to a variable
    with open(md_terminos, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown content to HTML
    html_content = markdown.markdown(md_content, output_format='html')
    return render(request, "core/terminos.html", {"content": html_content})

@require_safe
def privacidad(request):
    """
    This view is used to display the privacity page
    """
    # Ruta md
    md_privacidad = os.path.join(
        settings.STATICFILES_DIRS[2], "core/docs", "privacidad.md"
        )

    # Open the file and save its content to a variable
    with open(md_privacidad, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown content to HTML
    html_content = markdown.markdown(md_content, output_format='html')
    return render(request, "core/privacidad.html", {"content": html_content})
