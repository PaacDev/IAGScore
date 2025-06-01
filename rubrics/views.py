"""Views for the rubrics app."""

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator
from .forms import RubricForm
from .models import Rubric

@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def rubric_page(request):
    """
    View for import a new rubric.

    - GET: Displays the form.
    - POST: Processes the form and create new rubric.

    Parameters:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered template with the rubric form and rubric list.
    """
    query = request.GET.get("q", "")
    sort_field = request.GET.get("sort", "creation_date")
    sort_dir = request.GET.get("dir", "desc")

    # Get the user's rubrics ordering them by creation date
    # and paginate them
    rubric_list = Rubric.objects.filter(
        user=request.user
    )  # .order_by("-creation_date")

    # Sort the rubric list based on the sort field and direction
    sort_prefix = "-" if sort_dir == "desc" else ""
    order_by_field = f"{sort_prefix}{sort_field}"

    # Filter the rubric list based on the query
    if query:
        rubric_list = rubric_list.filter(name__icontains=query)

    rubric_list = rubric_list.order_by(order_by_field)

    # Paginate the rubric list
    paginator = Paginator(rubric_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # If the request is a POST, process the form
    if request.method == "POST":
        # Get the form data and files
        form = RubricForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new rubric object with the form data
            rubric = Rubric(
                name=form.cleaned_data["name"],
                content=form.cleaned_data["rubric_file"],
                user=request.user,
            )
            try:
                # Save the rubric object to the database
                with transaction.atomic():
                    rubric.save()
                    messages.success(request, _("Rúbrica importada correctamente"))
                    rubric_list = rubric_list.order_by(order_by_field)
                    paginator = Paginator(rubric_list, 5)
                    page_number = request.GET.get("page")
                    page_obj = paginator.get_page(page_number)
                    return render(
                        request,
                        "rubrics/mis_rubricas.html",
                        {
                            "form": form,
                            "rubric_list": rubric_list,
                            "page_obj": page_obj,
                            "query": query,
                            "sort": sort_field,
                            "dir": sort_dir,
                        },
                    )
            except IntegrityError:
                # Handle the case where the rubric already exists

                messages.error(
                    request, _("Error al guardar la rúbrica: Rubrica ya existente")
                )
                return render(
                    request,
                    "rubrics/mis_rubricas.html",
                    {
                        "form": form,
                        "rubric_list": rubric_list,
                        "page_obj": page_obj,
                        "query": query,
                        "sort": sort_field,
                        "dir": sort_dir,
                    },
                )

        messages.error(request, form.errors.as_text())
    else:
        form = RubricForm()

    return render(
        request,
        "rubrics/mis_rubricas.html",
        {
            "form": form,
            "rubric_list": rubric_list,
            "page_obj": page_obj,
            "query": query,
            "sort": sort_field,
            "dir": sort_dir,
        },
    )


@login_required
@require_GET
def show_rubric(request, rubric_id):
    """
    View for showing a rubric

    Parameters:
        request: The HTTP request object.
        rubric_id: The ID of the rubric to show.

    Returns:
        HttpResponse: The rendered template with the rubric details.

    Raises:
        Http404: If the rubric does not exist.
    """
    try:
        rubric = Rubric.objects.get(id=rubric_id, user=request.user)
    except Rubric.DoesNotExist as exc:
        raise Http404(_("Rúbrica no encontrada")) from exc

    return render(request, "rubrics/rubric.html", {"rubric": rubric})


@login_required
@require_POST
def delete_rubric(request, rubric_id):
    """
    View for deleting a rubric

    Parameters:
        request: The HTTP request object.
        rubric_id: The ID of the rubric to delete.

    Returns:
        HttpResponse: A redirect to the rubric page.

    Raises:
        Http404: If the rubric does not exist.
    """
    try:
        rubric = Rubric.objects.get(id=rubric_id, user=request.user)
        rubric.delete()
        messages.success(request, _("Rúbrica eliminada correctamente"))
    except Rubric.DoesNotExist as exc:
        raise Http404(_("Rúbrica no encontrada")) from exc

    return redirect("rubrics_page")
