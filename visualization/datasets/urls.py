from django.urls import path
from datasets.views import DatasetsMainView, create_dataset
from django.contrib.auth.decorators import login_required
import datasets.views as dataset_views
urlpatterns = [
    path('', login_required(DatasetsMainView.as_view(),login_url='/login/')),
    path('create_dataset/', create_dataset),
    path('<int:ex_id>/', dataset_views.detail, name='detail'),
    #path('upload_model/upload/', login_required(CreateView.as_view(),login_url='/login/')),
    #path('upload_model/upload/', file_upload_view, name= 'upload-view'),
]