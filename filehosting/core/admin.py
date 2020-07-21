from django.contrib import admin

from .models import FileObject


class FileObjectAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at', 'expiration_at')


admin.site.register(FileObject, FileObjectAdmin)
