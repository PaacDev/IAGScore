"""
This module contains the asynchronous task
"""
import os
import logging
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils import timezone
from celery import shared_task
from langchain_ollama import OllamaLLM
from iagscore import settings
from .models import Correction

logger = logging.getLogger(__name__)


@shared_task
def ejecuta_evaluacion_llm(correction_id):
    """
    Run a evaluation task using a LLM

    Parameters:
        correction_id: The Id of the correction to run
    """

    try:
        correction_obj = Correction.objects.get(id=correction_id)

        model = "llama3"
        tareas_dict = {}
        base_path = settings.MEDIA_ROOT
        full_path = os.path.join(base_path, correction_obj.folder_path)
        # Read the files
        for filename in os.listdir(full_path):
            if not filename.startswith("response"):
                with open(
                    os.path.join(full_path, filename), "r", encoding="utf-8"
                ) as file:
                    tareas_dict[filename] = file.read()

        llm_model = OllamaLLM(model=model, format="json")

        location = os.path.join(base_path, correction_obj.folder_path, "response")

        fs = FileSystemStorage(location=location)

        response = llm_model.invoke(
            correction_obj.prompt.prompt +
            correction_obj.rubric.content +
            str(tareas_dict)
            )

        file_content = ContentFile(response)
        filename = "response.txt"

        if fs.exists(filename):
            fs.delete(filename)

        correction_obj.last_ejecution_date = timezone.now()
        correction_obj.running = False
        correction_obj.llm_model = model
        correction_obj.save()

        fs.save(filename, file_content)
        return response
    except Exception as e:
        print(f"Error executing task: {e}")
        raise
    except Correction.DoesNotExist:
        print(f"Error: Correction with id {correction_id} does not exist")
        raise
