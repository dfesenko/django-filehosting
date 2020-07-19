from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django.conf import settings

from .forms import UploadFileForm
from .models import FileObject

import magic


class IndexView(View):

    def get(self, request):
        upload_file_form = UploadFileForm()
        return render(request, 'index.html', {'upload_file_form': upload_file_form})

    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)

        if upload_file_form.is_valid():
            f = upload_file_form.save()
            return redirect('file-info', file_id=str(f.file))


class FileInfoView(View):
    pass


class FileDownloadView(View):

    def get(self, request):
        with open(settings.MEDIA_URL + int(self.kwargs['file_id']), 'rb') as f:
            file_data = f.read()

            # detect the required content type
            f.seek(0)
            mime_type = magic.from_buffer(f.read(30), mime=True)

            # sending response
            return HttpResponse(file_data, content_type=f'{mime_type}; charset=utf-8')
