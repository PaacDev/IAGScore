"""
This module contains the views for the rubrics app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib import messages
from django.db import IntegrityError
from .forms import RubricForm
from .models import Rubric


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def rubric_page(request):
    """
    View for import a new rubric.
    """
    rubric_list = Rubric.objects.filter(user=request.user)
    if request.method == "POST":
        form = RubricForm(request.POST, request.FILES)
        if form.is_valid():
            rubric = Rubric(
                name=form.cleaned_data["name"],
                content=form.cleaned_data["rubric_file"],
                user=request.user,
            )
            try:
                rubric.save()
                messages.success(request, "Rúbrica importada correctamente")
                return render(
                    request,
                    "rubrics/mis_rubricas.html",
                    {"form": form, "rubric_list": rubric_list},
                )
            except IntegrityError:
                messages.error(
                    request, "Error al guardar la rúbrica: Rubrica ya existente"
                )
                return render(request, "rubrics/mis_rubricas.html", {"form": form})

        messages.error(request, form.errors.as_text())
    else:
        form = RubricForm()

    return render(
        request, "rubrics/mis_rubricas.html", {"form": form, "rubric_list": rubric_list}
    )


@login_required
@require_GET
def show_rubric(request, rubric_id):
    """
    View for showing a rubric
    """
    try:
        rubric = Rubric.objects.get(id=rubric_id, user=request.user)
    except Rubric.DoesNotExist as exc:
        raise Http404("Rúbrica no encontrada") from exc

    return render(request, "rubrics/rubric.html", {"rubric": rubric})


@login_required
@require_GET
def delete_rubric(request, rubric_id):
    """
    View for deleting a rubric
    """
    rubric = get_object_or_404(Rubric, id=rubric_id, user=request.user)
    rubric.delete()
    messages.success(request, "Rúbrica eliminada correctamente")
    return redirect("rubrics_page")
