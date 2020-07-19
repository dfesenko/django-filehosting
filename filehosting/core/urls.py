from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('files/<str:file_id>/info/', views.FileInfoView.as_view(), name="file-info"),
    path('files/<str:file_id>/get/', views.FileInfoView.as_view(), name="file-get"),
]
