import os
import random
import string

from django.db import models


class FileObject(models.Model):
    @staticmethod
    def filename_generator(instance, filename):
        random_chars = [random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                        for _ in range(7)]
        return os.path.join('', ''.join(random_chars))

    file = models.FileField(upload_to=filename_generator)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiration_in = models.IntegerField()
