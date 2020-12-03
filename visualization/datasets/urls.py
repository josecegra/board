from django.urls import path
from datasets.views import DatasetsMainView, create_dataset
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(DatasetsMainView.as_view(),login_url='/login/')),
    path('create_dataset/', create_dataset),
    #path('upload_model/upload/', login_required(CreateView.as_view(),login_url='/login/')),
    #path('upload_model/upload/', file_upload_view, name= 'upload-view'),
]