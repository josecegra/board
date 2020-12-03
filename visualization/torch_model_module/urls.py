from django.urls import path
from torch_model_module.views import MainView, file_upload_view, TorchModelView, upload_model
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(MainView.as_view(),login_url='/login/')),
    path('upload_model/', upload_model),
    #path('upload_model/upload/', login_required(CreateView.as_view(),login_url='/login/')),
    path('upload_model/upload/', file_upload_view, name= 'upload-view'),
]