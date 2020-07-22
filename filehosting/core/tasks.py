from django.utils import timezone

from filehosting.celery import app
from .models import FileObject


@app.task
def remove_expired_files():
    expired_files = FileObject.objects.filter(expiration_at__lt=timezone.now()).delete()
    print(expired_files)
