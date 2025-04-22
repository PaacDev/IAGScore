"""
This module contain the tasks to celery
"""
import os
import logging
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils import timezone
from celery import shared_task
from langchain_ollama import OllamaLLM
from rubrics.models import Rubric
from prompts.models import Prompt
from .models import Correction


logger = logging.getLogger(__name__)

@shared_task
def ejecuta_evaluacion_llm(correction_id, prompt_id, rubric_id):
    """
    Run a evaluation task using a LLM
    
    Parameters:
        correction_id: The Id of the correction to run
        prompt_id: the ID of the prompt
        rubric_id: the ID of the rubric

    """ 

    # Define LLM model
    model = "llama3"

    tareas_dict = dict()
    correction_obj = Correction.objects.get(id=correction_id)
    prompt = Prompt.objects.get(id = prompt_id)
    rubric = Rubric.objects.get(id = rubric_id)

    base_path = "./media/"

    # Read the files
    for filename in os.listdir(base_path+correction_obj.folder_path):
        if not filename.startswith('response'):
            with open(base_path+correction_obj.folder_path+filename, 'r', encoding='utf-8') as file:
                # Add the file content to the dict
                tareas_dict[filename] = file.read()

    # Initialize an instance of the LLM
    llm_model = OllamaLLM(model=model, format='json')

    # Set the location
    location = os.path.join(base_path, correction_obj.folder_path, "response/")
    fs = FileSystemStorage(location=location)

    # Invoke the model and capture the response
    response = llm_model.invoke(prompt.prompt+rubric.content+str(tareas_dict))

    # Prepare the response content to be saved in a text file
    file_content = ContentFile(response)
    filename = "response.txt"

    # Overwrite the file if exist
    if fs.exists(filename):
        fs.delete(filename)
    
    # Update correction model
    correction_obj.last_ejecution_date = timezone.now()
    correction_obj.running = False
    correction_obj.llm_model = model
    correction_obj.save()

    # Save the response content to the file system
    fs.save(filename, file_content)
