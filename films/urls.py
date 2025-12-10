from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('add/', views.add_film, name='add_film'),
    path('films/', views.film_list, name='film_list'),
    path('upload/', views.upload_file, name='upload'),
    path('files/', views.file_list, name='files'),
    
    # Новые функции для работы с БД
    path('edit/<int:film_id>/', views.edit_film, name='edit_film'),
    path('delete/<int:film_id>/', views.delete_film, name='delete_film'),
    path('search/', views.search_films, name='search_films'),
]