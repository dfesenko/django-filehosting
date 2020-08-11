from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .forms import UploadFileForm
from .models import FileObject

import magic
import os
from datetime import datetime, timedelta


class IndexView(View):

    def get(self, request):
        upload_file_form = UploadFileForm()
        return render(request, 'core/index.html', {'upload_file_form': upload_file_form})

    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)

        if upload_file_form.is_valid():
            file_obj = upload_file_form.save()
            file_obj.expiration_at = datetime.now() + timedelta(minutes=upload_file_form.cleaned_data['expiration_in'])
            file_obj.save()
            return redirect('core:file-info', file_id=str(file_obj.file).split("/")[1])
        else:
            raise Http404("The file size must not exceed 50 MB.")


class FileInfoView(View):

    def get(self, request, file_id):

        file_obj = get_object_or_404(FileObject, file__contains=file_id)

        if file_obj.expiration_at > timezone.now():
            mins_to_expiration = (file_obj.expiration_at - timezone.now())

            secs_to_expiration = int(mins_to_expiration.total_seconds() % 60)
            mins_to_expiration = int(mins_to_expiration.total_seconds() // 60)

            secs_to_expiration = "0" + str(secs_to_expiration) if secs_to_expiration < 10 else secs_to_expiration
            mins_to_expiration = "0" + str(mins_to_expiration) if mins_to_expiration < 10 else mins_to_expiration

            split_path = str(file_obj).split("/")

            file_id = split_path[1]

            file_size = f"{str(round(file_obj.file.size / 1000, 2))} KB" if file_obj.file.size < 1000000 \
                else f"{str(round(file_obj.file.size / 1000000, 2))} MB"

            filename = split_path[-1]

            expiration_at = file_obj.expiration_at

            return render(request, 'core/file-info.html', {'file_id': file_id,
                                                           'file_size': file_size,
                                                           'filename': filename,
                                                           'expiration_at': expiration_at,
                                                           'minutes_to_expiration': mins_to_expiration,
                                                           'seconds_to_expiration': secs_to_expiration})
        else:
            raise Http404("File does not exist")


class FileDownloadView(View):

    def get(self, request, file_id):

        file_obj = get_object_or_404(FileObject, file__contains=file_id)

        if file_obj.expiration_at > timezone.now():
            file_id = str(self.kwargs['file_id'])
            filename = os.listdir(settings.MEDIA_URL + file_id)[0]
            file_path = f"{settings.MEDIA_URL}{file_id}/{filename}"
            with open(file_path, 'rb') as f:
                file_data = f.read()

                # detect the required content type
                f.seek(0)
                mime_type = magic.from_buffer(f.read(30), mime=True)

                print(mime_type)

                # sending response
                return HttpResponse(file_data, content_type=f'{mime_type}; charset=utf-8')
        else:
            raise Http404("File does not exist")
