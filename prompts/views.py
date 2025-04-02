"""
This file contains the views for the prompts app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib import messages
from django.db import IntegrityError
from .forms import PromptForm
from .models import Prompt


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def prompt_page(request):
    """
    View for creating a new prompt.
    """
    prompt_list = Prompt.objects.filter(user=request.user)
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = Prompt(
                name=form.cleaned_data["name"],
                prompt=form.cleaned_data["prompt"],
                user=request.user,
            )

            try:
                prompt.save()
            except IntegrityError:
                messages.error(
                    request, "Error al guardar el prompt: Prompt ya existente"
                )
                return render(request, "prompts/prompts_page.html", {"form": form})
            messages.success(request, "Prompt creado correctamente")
            return render(
                request,
                "prompts/mis_prompts.html",
                {"form": form, "prompt_list": prompt_list},
            )

        messages.error(request, form.errors.as_text())
    else:
        form = PromptForm()

    return render(
        request, "prompts/mis_prompts.html", {"form": form, "prompt_list": prompt_list}
    )

@login_required
@require_GET
def show_prompt(request, prompt_id):
    """
    View for showing a prompt
    """
    try:
        prompt = Prompt.objects.get(id=prompt_id, user=request.user)
    except Prompt.DoesNotExist as exc:
        raise Http404("Prompt no encontrado") from exc

    return render(request, "prompts/show_prompt.html", {"prompt": prompt})

@login_required
@require_GET
def delete_prompt(request, prompt_id):
    """
    View for deleting a prompt
    """
    prompt = get_object_or_404(Prompt, id=prompt_id, user=request.user)
    prompt.delete()
    messages.success(request, "Prompt eliminado correctamente")
    return redirect("prompts_page")
