from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_film, name='add_film'),
    path('films/', views.film_list, name='film_list'),
    path('upload/', views.upload_file, name='upload'),
    path('files/', views.file_list, name='files'),
]