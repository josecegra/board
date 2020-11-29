from django.urls import path
from uploader.views import MainView, file_upload_view

urlpatterns = [
    path('', MainView.as_view()),
    path('upload/', file_upload_view, name= 'upload-view'),
]