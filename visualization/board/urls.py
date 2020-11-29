from django.urls import path


from . import views

app_name = 'board'

urlpatterns = [
    # ex: /polls/
    path('', views.home, name='board'),
    #path('explorer', views.explorer, name='base'),
    # ex: /polls/5/
    #path('<int:img_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),

]

