from django.urls import path
from uploader.views import MainView, file_upload_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(MainView.as_view(),login_url='/login/')),
    path('upload/', file_upload_view, name= 'upload-view'),
]