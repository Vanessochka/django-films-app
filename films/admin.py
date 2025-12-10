from django.contrib import admin
from .models import Film

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'year', 'genre', 'created_at']
    list_filter = ['genre', 'year']
    search_fields = ['title', 'director']
    ordering = ['-created_at']