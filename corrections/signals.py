"""Signal handlers for the Correction model."""

import shutil
import os
import logging
from django.utils.translation import gettext as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from iagscore import settings
from .models import Correction

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=Correction)
def delete_correction_folder(sender, instance, **kwargs):
    """
    Delete the files in the folder associated with the correction
    when it is deleted.

    Parameters:
        sender (models.Model): The model class that sent the signal (`Correction`).
        instance (Correction): The instance of the `Correction` model being deleted.
        **kwargs: Additional keyword arguments passed by the signal.

    """

    base_path = settings.MEDIA_ROOT
    # Path to the folder to be deleted
    folder_path = os.path.join(base_path, instance.folder_path)

    # Check if the folder exists and is a directory
    # and delete it
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            logger.info(_("Carpeta eliminada: %s"), folder_path)
        except OSError as e:
            logger.error(_("Error al eliminar la carpeta %s: %s"), folder_path, e)

    else:
        logger.warning(_("La carpeta no existe o no es un directorio."))
