
from django.urls import path

from . import views

from explorer import views as explorer_views

urlpatterns = [
    path('', explorer_views.explorer, name='index'),
    path('<int:img_id>/', explorer_views.detail,name='detail'),

]