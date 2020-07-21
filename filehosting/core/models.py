import os
import random
import string

from django.db import models
from django.conf import settings


def filename_generator(instance, filename):
    random_chars = [random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for _ in range(7)]
    return os.path.join(settings.MEDIA_URL, ''.join(random_chars), filename)


class FileObject(models.Model):
    file = models.FileField(upload_to=filename_generator)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiration_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.file)
