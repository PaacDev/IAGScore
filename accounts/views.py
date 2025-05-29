"""Views for the accounts application."""

from django.utils.translation import gettext_lazy as _
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

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse (HttpResponse): The rendered profile page.
    """
    return render(request, "accounts/profile.html")


@require_http_methods(["POST", "GET"])
@csrf_protect
def register(request):
    """
    This view is used to register a new user.

    - GET: Displays the registration form.
    - POST: Processes the form and creates the user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse (HttpResponse): The rendered registration page or redirect to login.
    """

    # If method is POST, process the form
    if request.method == "POST":
        # Instanciate the form with the POST data
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # Save the user add a succes message and redirect to login
            user_form.save()
            # Add a success message and redirect to login
            messages.add_message(
                request, messages.SUCCESS, _("Usuario creado correctamente")
            )
            return redirect("login")
        # If the form is not valid, add an error message
        messages.add_message(request, messages.ERROR, user_form.errors.as_text())
    else:
        # If method is GET, create an empty form
        user_form = RegisterForm()

    return render(request, "accounts/register.html", {"user_form": user_form})
