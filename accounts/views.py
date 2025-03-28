"""
This file contains the views for the accounts app.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm


@require_safe
@login_required
def profile(request):
    """
    This view is used to display the user profile.
    """
    return render(request, "accounts/profile.html")

@require_http_methods(['POST', 'GET'])
@csrf_protect
def register(request):
    """
    This view is used to register a new user.
    - GET: Displays the registration form.
    - POST: Processes the form and creates the user.
    """

    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.add_message(
                request, messages.SUCCESS, "Usuario creado correctamente"
            )
            return redirect("login")

        messages.add_message(request, messages.ERROR, user_form.errors.as_text())
    else:
        user_form = RegisterForm()

    return render(request, "accounts/register.html", {"user_form": user_form})
