from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import models
import json
import os
import uuid
from .forms import FilmForm, UploadForm, FilmEditForm
from .models import Film

def home(request):
    return render(request, 'home.html')

def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            film_data = {
                'title': form.cleaned_data['title'],
                'director': form.cleaned_data['director'],
                'year': form.cleaned_data['year'],
                'genre': form.cleaned_data['genre']
            }
            
            # Получаем выбранный тип хранилища
            storage_type = form.cleaned_data['storage_type']
            
            if storage_type == 'file':
                # СОХРАНЕНИЕ В ФАЙЛ
                os.makedirs('media/uploads', exist_ok=True)
                filename = f"film_{uuid.uuid4().hex}.json"
                file_path = f'media/uploads/{filename}'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([film_data], f, indent=2, ensure_ascii=False)
                
                messages.success(request, f'Фильм сохранен в файл: {filename}')
                return redirect('files')
                
            else:  # storage_type == 'db'
                # СОХРАНЕНИЕ В БАЗУ ДАННЫХ С ПРОВЕРКОЙ ДУБЛИКАТОВ
                try:
                    # Пытаемся найти или создать фильм
                    film, created = Film.objects.get_or_create(
                        title=film_data['title'],
                        director=film_data['director'],
                        year=film_data['year'],
                        defaults={'genre': film_data['genre']}
                    )
                    
                    if created:
                        messages.success(request, 'Фильм успешно сохранен в базу данных!')
                    else:
                        messages.warning(request, 'Такой фильм уже существует в базе данных!')
                    
                    return redirect('film_list')
                    
                except Exception as e:
                    messages.error(request, f'Ошибка при сохранении в базу: {str(e)}')
                    return redirect('add_film')
                    
    else:
        form = FilmForm()
    
    return render(request, 'add_film.html', {'form': form})

def film_list(request):
    # Получаем параметр source из GET запроса (из файлов или из БД)
    source = request.GET.get('source', 'db')  # по умолчанию из БД
    
    films = []
    source_name = ""
    
    if source == 'files':
        # ПОКАЗЫВАЕМ ИЗ ФАЙЛОВ
        source_name = "файлов"
        if os.path.exists('media/uploads'):
            for filename in os.listdir('media/uploads'):
                if filename.endswith('.json') and filename.startswith('film_'):
                    file_path = f'media/uploads/{filename}'
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        films.extend(data)
                    except:
                        continue
    else:
        # ПОКАЗЫВАЕМ ИЗ БАЗЫ ДАННЫХ
        source_name = "базы данных"
        films = list(Film.objects.all().order_by('-created_at').values())
    
    return render(request, 'film_list.html', {
        'films': films, 
        'source': source,
        'source_name': source_name
    })

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            storage_type = form.cleaned_data['storage_type']
            
            # Сохраняем файл
            os.makedirs('media/uploads', exist_ok=True)
            original_name = file.name
            ext = original_name.split('.')[-1]
            safe_name = f"upload_{uuid.uuid4().hex}.{ext}"
            file_path = f'media/uploads/{safe_name}'
            
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # Проверяем валидность JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Проверяем структуру
                if not isinstance(data, list):
                    raise ValueError("JSON должен быть массивом")
                
                for item in data:
                    if not all(key in item for key in ['title', 'director', 'year', 'genre']):
                        raise ValueError("Отсутствуют обязательные поля")
                
                # Если выбрано сохранение в БД
                if storage_type == 'db':
                    imported_count = 0
                    duplicate_count = 0
                    
                    for item in data:
                        try:
                            film, created = Film.objects.get_or_create(
                                title=item['title'],
                                director=item['director'],
                                year=item['year'],
                                defaults={'genre': item['genre']}
                            )
                            if created:
                                imported_count += 1
                            else:
                                duplicate_count += 1
                        except:
                            duplicate_count += 1
                    
                    messages.success(request, 
                        f'Импортировано {imported_count} фильмов. '
                        f'Пропущено дубликатов: {duplicate_count}'
                    )
                    # Удаляем временный файл так как данные в БД
                    os.remove(file_path)
                    
                else:
                    messages.success(request, f'Файл {safe_name} успешно загружен')
                
                return redirect('files' if storage_type == 'file' else 'film_list')
                
            except Exception as e:
                # Удаляем невалидный файл
                if os.path.exists(file_path):
                    os.remove(file_path)
                return render(request, 'upload.html', {
                    'form': form, 
                    'error': f'Неверный формат файла: {str(e)}'
                })
    else:
        form = UploadForm()
    
    return render(request, 'upload.html', {'form': form})

def file_list(request):
    files = []
    if os.path.exists('media/uploads'):
        for filename in os.listdir('media/uploads'):
            if filename.endswith('.json'):
                file_path = f'media/uploads/{filename}'
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    content = json.dumps(data, indent=2, ensure_ascii=False)
                    files.append({'name': filename, 'content': content})
                except:
                    files.append({'name': filename, 'content': 'Ошибка чтения файла'})
    
    return render(request, 'files.html', {'files': files})

# НОВЫЕ ФУНКЦИИ ДЛЯ РЕДАКТИРОВАНИЯ И УДАЛЕНИЯ
def edit_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    
    if request.method == 'POST':
        form = FilmEditForm(request.POST, instance=film)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Фильм успешно обновлен!')
                return redirect('film_list')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении: {str(e)}')
    else:
        form = FilmEditForm(instance=film)
    
    return render(request, 'edit_film.html', {'form': form, 'film': film})

def delete_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    
    if request.method == 'POST':
        film_title = film.title
        film.delete()
        messages.success(request, f'Фильм "{film_title}" удален!')
        return redirect('film_list')
    
    return render(request, 'delete_film.html', {'film': film})

# AJAX ПОИСК
def search_films(request):
    query = request.GET.get('q', '')
    
    if query:
        films = Film.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(director__icontains=query) |
            models.Q(genre__icontains=query)
        ).values('id', 'title', 'director', 'year', 'genre')
    else:
        films = Film.objects.all().values('id', 'title', 'director', 'year', 'genre')
    
    films_list = list(films)
    return JsonResponse({'films': films_list})