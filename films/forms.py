from django import forms
from .models import Film

class FilmForm(forms.ModelForm):
    # Добавляем поле выбора хранилища
    STORAGE_CHOICES = [
        ('file', 'Сохранить в файл'),
        ('db', 'Сохранить в базу данных'),
    ]
    storage_type = forms.ChoiceField(
        choices=STORAGE_CHOICES, 
        label='Куда сохранить',
        initial='file',
        widget=forms.RadioSelect  # Радиокнопки вместо выпадающего списка
    )
    
    class Meta:
        model = Film
        fields = ['title', 'director', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название фильма',
            'director': 'Режиссер',
            'year': 'Год выпуска', 
            'genre': 'Жанр',
        }

class UploadForm(forms.Form):
    file = forms.FileField(label='Выберите JSON файл')
    
    # Добавляем выбор куда сохранить загруженные данные
    STORAGE_CHOICES = [
        ('file', 'Оставить в файле'),
        ('db', 'Импортировать в базу данных'),
    ]
    storage_type = forms.ChoiceField(
        choices=STORAGE_CHOICES,
        label='Куда сохранить загруженные данные',
        initial='file',
        widget=forms.RadioSelect
    )

# Форма для редактирования (без выбора хранилища)
class FilmEditForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'director', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
        }