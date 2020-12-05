from django.urls import path
from experiments.views import ExperimentsMainView, create_experiment
from django.contrib.auth.decorators import login_required
import experiments.views as experiments_views
from explorer import views as explorer_views
from datasets import views as dataset_views

urlpatterns = [
    path('', login_required(ExperimentsMainView.as_view(),login_url='/login/')),
    path('create_experiment/', create_experiment),
    path('<int:ex_id>/', experiments_views.detail_experiment, name='detail'),
    path('<int:ex_id>/<int:img_id>/', experiments_views.detail_image, name='detail_image'),
    
    #path('upload_model/upload/', login_required(CreateView.as_view(),login_url='/login/')),
    #path('upload_model/upload/', file_upload_view, name= 'upload-view'),
]