"""Views for the corrections app."""

import shutil
import tempfile
import os
import logging
import ollama
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import Http404, FileResponse
from django.contrib import messages
from django.db.models import Q
from pyunpack import Archive
from iagscore import settings
from prompts.models import Prompt
from rubrics.models import Rubric
from .forms import CorrectionForm
from .models import Correction
from .tasks import start_llm_evaluation

logger = logging.getLogger(__name__)


def process_zip_file(archive_path, user, id_correction):
    """
    Process the ZIP file containing Java files and save them.

    Parameters:
        archive_file: File to proceess
        user: User that making te request
        id_correction: The id to the correction

    Returns
        str: The path where the files were saved.
    """

    # Get the file extension
    ext = os.path.splitext(archive_path.name)[1]

    # If it's a Django UploadedFile, save it to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        for chunk in archive_path.chunks():
            tmp.write(chunk)
        archive_path = tmp.name

    base_path = settings.MEDIA_ROOT
    folder_path = f"corrections/{user.id}/{id_correction}/"
    full_path = os.path.join(base_path, folder_path)
    # Ensure the directory exists
    os.makedirs(full_path, exist_ok=True)

    fs = FileSystemStorage(location=full_path)

    temp_extract_path = os.path.join(full_path, "temp_extract")
    # Ensure the directory exists
    os.makedirs(temp_extract_path, exist_ok=True)

    # Extract the compressed file
    Archive(archive_path).extractall(temp_extract_path)

    # Delete non-Java files
    for root, dirs, files in os.walk(temp_extract_path):
        # Skip directories that start with "_" or "."
        dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]

        for file in files:
            logger.info("Processing file: %s", file)
            # Check if the file is a Java file
            if file.endswith(".java") and not file.startswith(("_", ".")):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    # Save the file
                    fs.save(file, f)

    # Remove the temporary extraction directory
    shutil.rmtree(temp_extract_path)

    return folder_path


@login_required
@require_GET
def run_model(request, correction_id):
    """
    Call the task to run the model in async mode

    Parameters:
        request (HttpRequest): The HTTP request object.
        correction_id (int): The ID of the correction to process.

    Returns:
        HttpResponse: A redirect to the correction detail view after queuing the task.

    Raises:
        Http404: If the correction with the given ID does not exist.
        Exception: If an error occurs while processing the correction.
    """
    try:

        correction_obj = Correction.objects.get(id=correction_id)
        correction_obj.running = True
        correction_obj.save()

        models = ollama.list()
        model_names = [model["model"] for model in models["models"]]

        if correction_obj.llm_model not in model_names:
            correction_obj.running = False
            correction_obj.save()
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    "El modelo seleccionado para esta corrección no está cargado en Ollama."
                ),
            )
            return redirect("show_view_correction")

        # Initiate the task asynchronously
        start_llm_evaluation.delay(correction_id)

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Corrección en proceso. Revisa el resultado más tarde."),
        )

    except Correction.DoesNotExist as exc:
        logger.error("Error: Correction with id %s does not exist", correction_id)
        raise Http404(_("Corrección no encontrada.")) from exc

    return redirect("show_view_correction")


@login_required
@require_GET
def download_response(request, correction_id):
    """
    Download the file whit the response if exist

    Parameters:
        request:
        correction_id: The ID of the correction

    Return:
        FileResponse: the file to download

    Raises:
        Http404: If the correction with the given ID does not exist or if the file does not exist.
    """

    try:
        correction_obj = Correction.objects.get(id=correction_id)
    except Correction.DoesNotExist as exc:
        raise Http404(_("Corrección no encontrada.")) from exc

    # Absolute path to the file
    base_path = settings.MEDIA_ROOT
    file_path = os.path.join(
        base_path, correction_obj.folder_path, "response", "response.txt"
    )

    if not os.path.exists(file_path):
        raise Http404(_("El archivo no existe."))

    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="response.txt"
    )


@login_required
@require_POST
@csrf_protect
def delete_correction(request, item_id):
    """
    Delete one correction

    Parameters:
        request: the HTTP request object
        id: The id of the correction

    Return:
        HttpResponse: A redirect to the corrections view.

    Raises:
        Http404: If the correction with the given ID does not exist.
        Exception: If an error occurs while deleting the correction.
    """

    try:
        correction_obj = Correction.objects.get(id=item_id)
        correction_obj.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            _("Corrección: %s, eliminada correctamente." % correction_obj.description),
        )
    except Correction.DoesNotExist as exc:
        raise Http404(_("Corrección no encontrada.")) from exc

    return redirect("show_view_correction")


@login_required
@csrf_protect
@require_http_methods(["POST", "GET"])
def show_new_correction(request):
    """
    View to display the form for creating a new correction.

    - GET: Displays the form.
    - POST: Processes the form and create new correction.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template for creating a new correction
                    or a redirect to the view correction page.
    """
    # Check if there is any clone data in the session
    clone_data = request.session.pop("correction_clone_data", None)

    # Get the user's rubrics and prompts
    rubric_list = Rubric.objects.filter(user=request.user)
    prompt_list = Prompt.objects.filter(user=request.user)
    # Get the selected rubric and prompt id from the request
    rubric_select_id = request.GET.get("rubric_id")
    prompt_selected_id = request.GET.get("prompt_id")
    # Initialize the correction form
    # correct_form = CorrectionForm()
    correct_form = (
        CorrectionForm(initial=clone_data) if clone_data else CorrectionForm()
    )
    # Initialize the selected rubric and prompt
    rubric_select = None
    prompt_select = None

    if clone_data:
        rubric_select_id = clone_data.get("rubric")
        prompt_selected_id = clone_data.get("prompt")

    # Get the list of models pulled from Ollama
    models = ollama.list()
    model_names = [model["model"] for model in models["models"]]

    # If rubric_select_id or prompt_selected_id are not None, get the objects
    if rubric_select_id:
        rubric_select = Rubric.objects.get(id=rubric_select_id)

    if prompt_selected_id:
        prompt_select = Prompt.objects.get(id=prompt_selected_id)

    # If the request method is POST, process the form
    if request.method == "POST":
        # Instantiate the form with the POST data and files
        correct_form = CorrectionForm(request.POST, request.FILES)
        if correct_form.is_valid():
            # Process the correction object without commit
            # to set the folder path using the user id
            new_corrections = correct_form.save(commit=False)
            new_corrections.user = request.user
            # Save the correction object to get the id
            new_corrections.save()

            # Process the zip file and save its content
            # and set the folder path
            path = process_zip_file(
                request.FILES["zip_file"], request.user, new_corrections.id
            )
            new_corrections.folder_path = path
            new_corrections.save()
            # Sucess message
            messages.add_message(
                request, messages.SUCCESS, _("Corrección creada correctamente")
            )
            # Redirect to the view correction page
            return redirect("show_view_correction")
        # If the form is not valid, log the errors
        else:
            messages.add_message(request, messages.ERROR, _("Error al crear correción"))
            errors = correct_form.errors.as_data()

            # Save the error in messages
            for field, error_list in errors.items():
                for error in error_list:
                    logger.error("Error en el campo %s: %s", field, error.message)
                    if field == 'llm_model':
                        field = _("Modelo")
                    elif field == 'rubric':
                        field = _("Rúbrica")
                    elif field == 'prompt':
                        field = ("Prompt")
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"Error en el campo '{field}': {error.message}",
                    )
            # Redirect to the view correction page
            return redirect("show_new_correction")

    return render(
        request,
        "corrections/new_correction.html",
        {
            "rubric_list": rubric_list,
            "prompt_list": prompt_list,
            "rubric_select": rubric_select,
            "prompt_select": prompt_select,
            "correct_form": correct_form,
            "model_names": model_names,
        },
    )


@login_required
@require_GET
def show_view_correction(request):
    """
    Show the view of the corrections table

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template for the corrections table.
    """

    query = request.GET.get("q", "")
    sort_field = request.GET.get("sort", "date")
    sort_dir = request.GET.get("dir", "desc")

    # Get the correction list for the user ordered by date
    # and paginate the results
    correction_list = Correction.objects.filter(user=request.user)

    # Sort the correction list based on the sort field and direction
    sort_prefix = "-" if sort_dir == "desc" else ""
    order_by_field = f"{sort_prefix}{sort_field}"

    # Filter the correction list based on the query
    if query:
        correction_list = correction_list.filter(description__icontains=query)

    # If the sort field is "last_ejecution_date", filter out None values ("never executed")
    if sort_field == "last_ejecution_date":
        correction_list = correction_list.filter(~Q(last_ejecution_date=None))

    # Order the correction list based on the sort field
    correction_list = correction_list.order_by(order_by_field)

    paginator = Paginator(correction_list, 5)
    page_number = request.GET.get("page")
    corrections_obj = paginator.get_page(page_number)

    return render(
        request,
        "corrections/view_correction.html",
        {
            "page_obj": corrections_obj,
            "query": query,
            "sort": sort_field,
            "dir": sort_dir,
        },
    )


@login_required
@require_GET
def corrections(request):
    """
    Show the corrections base page

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template for the corrections base page.
    """
    return render(request, "corrections/correction_base.html")


@login_required
@require_GET
def correction_clone(request, item_id):
    """
    Clone a correction object.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The primary key of the correction to clone.

    Returns:
        HttpResponse: A redirect to the view correction page after cloning.

    Raises:
        Http404: If the correction with the given ID does not exist.
    """
    try:
        correction = Correction.objects.get(pk=item_id, user=request.user)

        # Prepare the initial data for the clone
        initial_data = {
            "description": correction.description,
            "llm_model": correction.llm_model,
            "model_temp": correction.model_temp,
            "model_top_p": correction.model_top_p,
            "model_top_k": correction.model_top_k,
            "output_format": correction.output_format,
            "rubric": correction.rubric.id if correction.rubric else None,
            "prompt": correction.prompt.id if correction.prompt else None,
        }

        request.session["correction_clone_data"] = initial_data
        messages.add_message(
            request,
            messages.INFO,
            _(
                "Datos clonados de la corrección: %s. Puedes editarlos antes de crear una nueva corrección. Debes incluir un archivo comprimido con las tareas"
            )
            % correction.description,
        )
    except Correction.DoesNotExist as exc:
        raise Http404(_("Corrección no encontrada.")) from exc

    return redirect("show_new_correction")
