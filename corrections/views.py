"""
This module contains views for the corrections app.
"""

import zipfile
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.contrib import messages
from prompts.models import Prompt
from rubrics.models import Rubric
from .forms import CorrectionForm
from .models import Correction


@login_required
@require_http_methods(["POST", "GET"])
@csrf_protect
def corrections(request):
    """
    View to display corrections.
    """
    rubric_list = Rubric.objects.filter(user=request.user)
    prompt_list = Prompt.objects.filter(user=request.user)
    correction_list = Correction.objects.filter(user=request.user)
    rubric_select_id = request.GET.get("rubric_id")
    prompt_selected_id = request.GET.get("prompt_id")
    correct_form = CorrectionForm()
    rubric_select = None
    prompt_select = None

    if rubric_select_id:
        rubric_select = Rubric.objects.get(id=rubric_select_id)

    if prompt_selected_id:
        prompt_select = Prompt.objects.get(id=prompt_selected_id)

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "save_correction":
            correct_form = CorrectionForm(request.POST, request.FILES)
            if correct_form.is_valid():
                new_corrections = correct_form.save(commit=False)
                new_corrections.user = request.user
                new_corrections.save()
                path = procesar_ficheros(
                    request.FILES["zip_file"], request.user, new_corrections.id
                )
                new_corrections.folder_path = path
                new_corrections.save()
                messages.add_message(
                    request, messages.SUCCESS, "Correción creada correctamente"
                )
            else:
                messages.add_message(
                    request, messages.ERROR, "Error al crear correción"
                )
                print(correct_form.errors.get_context())

    return render(
        request,
        "corrections/corrections.html",
        {
            "corrections": correction_list,
            "rubric_list": rubric_list,
            "prompt_list": prompt_list,
            "rubric_select": rubric_select,
            "prompt_select": prompt_select,
            "correct_form": correct_form,
        },
    )


def show_correction(request, correction_id):
    """
    view for showing a correction
    """
    try:
        correction = Correction.objects.get(id=correction_id, user=request.user)
    except Correction.DoesNotExist as exc:
        raise Http404("Rúbrica no encontrada") from exc

    return render(
        request, "corrections/show_correction.html", {"correction": correction}
    )


def procesar_ficheros(zip_file, user, id_correction):
    """
    Process the uploaded files.
    """
    print("Processing files...")

    folder_path = f"corrections/{user.id}/{id_correction}/"
    full_path = os.path.join("media", folder_path)

    fs = FileSystemStorage(location=full_path)

    # Unzip the file
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        files_list = zip_ref.namelist()
        entregas = [
            f
            for f in files_list
            if f.endswith(".java") and not f.startswith(("_", "."))
        ]

        for file in entregas:
            with zip_ref.open(file) as extracted_file:
                fs.save(file, extracted_file)

    return folder_path
