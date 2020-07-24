from django.utils import timezone

from filehosting.celery import app
from .models import FileObject

import shutil
import os


@app.task
def remove_expired_files():
    expired_files = FileObject.objects.filter(expiration_at__lt=timezone.now())

    for file in expired_files:
        path_to_file = os.path.join(os.getcwd(), str(file))
        path_to_file_directory = "/".join(path_to_file.split("/")[:-1])
        shutil.rmtree(path_to_file_directory, ignore_errors=True)

    expired_files.delete()
