
from django.urls import path

from . import views

urlpatterns = [
    path('', views.explorer, name='index'),
    path('<int:img_id>/', views.detail, name='detail'),

]