"""Views for the corrections app."""
import zipfile
import os
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import Http404, FileResponse
from django.contrib import messages
from iagscore import settings
from prompts.models import Prompt
from rubrics.models import Rubric
from .forms import CorrectionForm
from .models import Correction
from .tasks import start_llm_evaluation

logger = logging.getLogger(__name__)


def process_zip_file(zip_file, user, id_correction):
    """
    Process the ZIP file containing Java files and save them.

    Parameters:
        zip_file: File to proceess
        user: User that making te request
        id_correction: The id to the correction

    Returns
        str: The path where the files were saved.
    """

    base_path = settings.MEDIA_ROOT
    folder_path = f"corrections/{user.id}/{id_correction}/"
    full_path = os.path.join(base_path, folder_path)

    # File system storage object pointing to the specified path
    fs = FileSystemStorage(location=full_path)

    # Unzip the file
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        files_list = zip_ref.namelist()
        # List of files .java
        entregas = [
            file
            for file in files_list
            if file.endswith(".java") and not file.startswith(("_", "."))
        ]

        # Save the java files in the full_path
        for file in entregas:
            filename_only = os.path.basename(file)  # Add only the files
            with zip_ref.open(file) as extracted_file:
                # Save the extracted file
                fs.save(filename_only, extracted_file)

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

        # Initiate the task asynchronously
        start_llm_evaluation.delay(correction_id)
    except Correction.DoesNotExist as exc:
        logger.error("Error: Correction with id %s does not exist", correction_id)
        raise Http404("Corrección no encontrada.") from exc

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
        raise Http404("Corrección no encontrada.") from exc

    # Absolute path to the file
    base_path = settings.MEDIA_ROOT
    file_path = os.path.join(
        base_path, correction_obj.folder_path, "response", "response.txt"
    )

    if not os.path.exists(file_path):
        raise Http404("El archivo no existe.")

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
    except Correction.DoesNotExist as exc:
        raise Http404("Corrección no encontrada.") from exc

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
    # Get the user's rubrics and prompts
    rubric_list = Rubric.objects.filter(user=request.user)
    prompt_list = Prompt.objects.filter(user=request.user)
    # Get the selected rubric and prompt id from the request
    rubric_select_id = request.GET.get("rubric_id")
    prompt_selected_id = request.GET.get("prompt_id")
    # Initialize the correction form
    correct_form = CorrectionForm()
    # Initialize the selected rubric and prompt
    rubric_select = None
    prompt_select = None

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
                request, messages.SUCCESS, "Correción creada correctamente"
            )
        # If the form is not valid, log the errors
        else:
            messages.add_message(request, messages.ERROR, "Error al crear correción")
            errors = correct_form.errors.as_data()

            # Save the error in messages
            for field, error_list in errors.items():
                for error in error_list:
                    logger.error("Error en el campo %s: %s",field, error.message)
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"Error en el campo '{field}': {error.message}",
                    )
        # Redirect to the view correction page
        return redirect("show_view_correction")

    return render(
        request,
        "corrections/new_correction.html",
        {
            "rubric_list": rubric_list,
            "prompt_list": prompt_list,
            "rubric_select": rubric_select,
            "prompt_select": prompt_select,
            "correct_form": correct_form,
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
    # Get the correction list for the user ordered by date
    # and paginate the results
    correction_list = Correction.objects.filter(user=request.user).order_by("-date")
    paginator = Paginator(correction_list, 5)
    page_number = request.GET.get("page")
    corrections_obj = paginator.get_page(page_number)

    return render(
        request,
        "corrections/view_correction.html",
        {
            "corrections": corrections_obj,
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
