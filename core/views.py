from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import markdown


@login_required
def home(request):
    """
    This view is used to display the user profile.
    """
    return render(request, "core/home.html")


def terminos(request):
    # Ruta md
    md_terminos = os.path.join(settings.STATICFILES_DIRS[2], "core/docs", "terminos.md")
    with open(md_terminos, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)
    return render(request, "core/terminos.html", {"content": html_content})


def privacidad(request):
    # Ruta md
    md_privacidad = os.path.join(
        settings.STATICFILES_DIRS[2], "core/docs", "privacidad.md"
    )
    with open(md_privacidad, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)
    return render(request, "core/privacidad.html", {"content": html_content})
