"""
Views for the prompts app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator
from .forms import PromptForm
from .models import Prompt


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def prompt_page(request):
    """
    View for creating a new prompt.
    
    - GET: Displays the form.
    - POST: Processes the form and create new prompt.
    
    Parameters:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: The rendered template with the prompt form and prompt list.
    """
    query = request.GET.get('q',"")
    sort_field = request.GET.get("sort", "creation_date")
    sort_dir = request.GET.get("dir", "desc")

    # Get the user's prompts ordering them by creation date
    # and paginate them
    prompt_list = Prompt.objects.filter(user=request.user)#.order_by("-creation_date")

    # Sort the prompt list based on the sort field and direction
    sort_prefix = "-" if sort_dir == "desc" else ""
    order_by_field = f"{sort_prefix}{sort_field}"

    # Filter the prompt list based on the query
    if query:
        prompt_list = prompt_list.filter(name__icontains=query)

    prompt_list = prompt_list.order_by(order_by_field)

    # Paginate the prompt list
    paginator = Paginator(prompt_list, 5)
    page_numer = request.GET.get("page")
    page_obj = paginator.get_page(page_numer)

    # If the request is a POST, process the form
    if request.method == "POST":
        # Get the form data
        form = PromptForm(request.POST)
        if form.is_valid():
            # Create a new prompt object with the form data
            prompt = Prompt(
                name=form.cleaned_data["name"],
                prompt=form.cleaned_data["prompt"],
                user=request.user,
            )

            try:
                # Save the prompt object to the database
                prompt.save()
                messages.success(request, "Prompt creado correctamente")
                prompt_list = list(Prompt.objects.filter(user=request.user))
                return render(
                    request,
                    "prompts/mis_prompts.html",
                    {"form": form, 
                     "prompt_list": prompt_list,
                     "page_obj": page_obj,
                     "query": query,
                     "sort": sort_field,
                     "dir": sort_dir,
                     },
                )
            except IntegrityError:
                # Handle the case where the prompt already exists
                messages.error(
                    request, "Error al guardar el prompt: Prompt ya existente"
                )
                return render(request, "prompts/mis_prompts.html", {"form": form})
        messages.error(request, form.errors.as_text())
    else:
        form = PromptForm()

    return render(
        request,
        "prompts/mis_prompts.html",
        {"form": form, "prompt_list": prompt_list, "page_obj": page_obj, "query": query, "sort": sort_field, "dir": sort_dir,},
    )


@login_required
@require_GET
def show_prompt(request, prompt_id):
    """
    View for showing a prompt
    
    Parameters:
        request: The HTTP request object.
        prompt_id: The ID of the prompt to show.
        
    Returns:
        HttpResponse: The rendered template with the prompt details.

    Raises:
        Http404: If the prompt does not exist.
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
    
    Parameters:
        request: The HTTP request object.
        prompt_id: The ID of the prompt to delete.
        
    Returns:
        HttpResponse: Redirects to the prompt page with a success message.
        
    Raises:
        Http404: If the prompt does not exist.
    """
    prompt = get_object_or_404(Prompt, id=prompt_id, user=request.user)
    prompt.delete()
    messages.success(request, "Prompt eliminado correctamente")
    return redirect("prompts_page")
