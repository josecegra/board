from django.urls import path
from experiments.views import ExperimentsMainView, create_experiment
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ExperimentsMainView.as_view(),login_url='/login/')),
    path('create_experiment/', create_experiment),
    #path('upload_model/upload/', login_required(CreateView.as_view(),login_url='/login/')),
    #path('upload_model/upload/', file_upload_view, name= 'upload-view'),
]