""" Views for the core application. """

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


@require_http_methods(["POST", "GET"])
@csrf_protect
def custom_login(request):
    """
    Custom user login.

    - GET: Displays the login form.
    - POST: Processes the form and login.

    Parameters:
        request(HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or redirect to home.
    """

    # If method is POST, process the form else show the form
    if request.method == "POST":
        # Instantiate the AuthenticationForm with the request and POST data
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            # If user is authenticated, log in and redirect to home
            if user:
                login(request, user)
                return redirect("home")
        # If user is not authenticated, show error message
        else:
            messages.add_message(
                request, messages.ERROR, "Usuario o contraseña incorrectos"
            )
    else:
        # If method is GET, show the login form
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

@require_GET
@login_required
def home(request):
    """
    Display the home page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse : The rendered home page.
    """
    return render(request, "core/home.html")

@require_GET
def logout_view(request):
    """
    Logout the user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse : Redirects to the login page.
    """
    logout(request)
    return redirect("login")


@require_safe
def terminos(request):
    """
    Display the terms and conditions page

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse : The rendered terms and conditions page.
    """
    # Path md terminos
    md_terminos = os.path.join(settings.STATICFILES_DIRS[2], "core/docs", "terminos.md")

    # Open the file and save its content to a variable
    with open(md_terminos, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown content to HTML and render it
    html_content = markdown.markdown(md_content, output_format="html")
    return render(request, "core/terminos.html", {"content": html_content})


@require_safe
def privacidad(request):
    """
    Display the privacity page

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered privacy page.
    """
    # Path md
    md_privacidad = os.path.join(
        settings.STATICFILES_DIRS[2], "core/docs", "privacidad.md"
    )

    # Open the file and save its content to a variable
    with open(md_privacidad, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown content to HTML and render it
    html_content = markdown.markdown(md_content, output_format="html")
    return render(request, "core/privacidad.html", {"content": html_content})

@require_safe
def llm_section(request):
    """
    Display llm section

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered llm section page.
    """

    return render(request, "core/llm_info.html")
