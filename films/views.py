from django.shortcuts import render, redirect
from .forms import FilmForm, UploadForm
from .models import Film
import json
import os
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            film = form.save()
            
            films_data = []
            for f in Film.objects.all():
                films_data.append({
                    'title': f.title,
                    'director': f.director,
                    'year': f.year,
                    'genre': f.genre
                })
            
            os.makedirs('media/uploads', exist_ok=True)
            
            with open('media/uploads/films.json', 'w', encoding='utf-8') as f:
                json.dump(films_data, f, indent=2, ensure_ascii=False)
            
            return redirect('film_list')
    else:
        form = FilmForm()
    
    return render(request, 'add_film.html', {'form': form})

def film_list(request):
    films = Film.objects.all()
    return render(request, 'film_list.html', {'films': films})

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            os.makedirs('media/uploads', exist_ok=True)
            file_path = 'media/uploads/uploaded.json'
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    Film.objects.create(
                        title=item['title'],
                        director=item['director'],
                        year=item['year'],
                        genre=item['genre']
                    )
                
                return redirect('film_list')
            except Exception as e:
                if os.path.exists(file_path):
                    os.remove(file_path)
                return render(request, 'upload.html', {'form': form, 'error': f'Неверный формат файла: {str(e)}'})
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
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        files.append({'name': filename, 'content': content})
                    except:
                        files.append({'name': filename, 'content': 'Ошибка чтения файла'})
    
    return render(request, 'files.html', {'files': files})