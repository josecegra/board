from django.urls import path,re_path
from datasets.views import DatasetsMainView, create_dataset
from django.contrib.auth.decorators import login_required
import datasets.views as dataset_views

urlpatterns = [
    path('', login_required(DatasetsMainView.as_view(),login_url='/login/')),
    path('create_dataset/', create_dataset),
    path('<int:ex_id>/', dataset_views.detail_dataset, name='detail'),
    path('<int:dt_id>/<int:img_id>/', dataset_views.detail_image, name='detail_image'),
]