from django import forms

from django.conf import settings
from . import models


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = models.FileObject
        fields = ('file',)

    file = forms.FileField(required=True)
    expiration_in = forms.IntegerField(min_value=1, max_value=5, required=True, label='Minutes to expiration')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > settings.MAX_SIZE:
            raise forms.ValidationError("The file size must not exceed 50 MB.")
        return file
