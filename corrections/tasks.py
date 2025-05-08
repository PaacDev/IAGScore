"""This module contains the asynchronous task"""
import os
import logging
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils import timezone
from celery import shared_task
from langchain_ollama import OllamaLLM
from iagscore import settings
from .models import Correction

# Configure logging
logger = logging.getLogger(__name__)


@shared_task
def ejecuta_evaluacion_llm(correction_id):
    """
    Run a evaluation task using a LLM

    Parameters:
        correction_id (int): The Id of the correction to evaluate
    
    Raises:
        Exception: If the correction object does not exist or if there is an error during execution.
        Correction.DoesNotExist: If the correction object does not exist.
    """

    try:
        # Get the correction object
        correction_obj = Correction.objects.get(id=correction_id)

        model = "llama3"
        base_path = settings.MEDIA_ROOT
        tasks_dict = set_tasks_dict(correction_obj.folder_path)

        # Set the model name and parameters
        llm_model = OllamaLLM(
            model=model, format="json",
            temperature=correction_obj.model_temp,
            top_p=correction_obj.model_top_p,
            top_k=correction_obj.model_top_k
            )

        # Set the location for storing the response file
        location = os.path.join(base_path, correction_obj.folder_path, "response")

        # Initialize the file storage system at the specified location
        fs = FileSystemStorage(location=location)

        # Invoke the LLM model with the prompt, rubric and tasks
        response = llm_model.invoke(
            correction_obj.prompt.prompt +
            correction_obj.rubric.content +
            str(tasks_dict)
            )

        # Create a file system storage object
        file_content = ContentFile(response)
        filename = "response.txt"

        # Delete the previous response file if it exists
        if fs.exists(filename):
            fs.delete(filename)

        # Update the correction object
        correction_obj.last_ejecution_date = timezone.now()
        correction_obj.running = False
        correction_obj.llm_model = model
        correction_obj.save()

        # Save the response to a file
        fs.save(filename, file_content)
        return response

    except Correction.DoesNotExist:
        logger.error("Error: Correction with id %s does not exist", correction_id)
        raise
    except Exception as e:
        logger.error("Error executing task: %s",e)
        correction_obj.running = False
        correction_obj.save()
        raise

def set_tasks_dict(folder_path):
    """
    Set the tasks dictionary with the tasks in folder path for evaluation

    Parameters:
        folder_path: The path to the folder containing the task files.
        
    Returns:
        dict: A dictionary where the keys are filenames and the values are the file contents.
    """

    tasks_dict= {}

    # Path to the folder where the files are stored
    full_path = os.path.join(settings.MEDIA_ROOT, folder_path)

    try:
        # Read the files in the directory
        for filename in os.listdir(full_path):
            # Skip files or directories starting with "response"
            if not filename.startswith("response"):
                # Read the file and store its content in the dictionary
                with open(os.path.join(full_path, filename), "r", encoding="utf-8") as file:
                    tasks_dict[filename] = file.read()
    except FileNotFoundError:
        logger.exception("Error: The folder %s was not found.", full_path)
    except PermissionError:
        logger.exception("Error: Insufficient permissions to access the folder %s.",full_path)

    return tasks_dict
