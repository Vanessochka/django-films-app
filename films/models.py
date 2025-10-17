from django.db import models

class Film(models.Model):
    title = models.CharField('Название фильма', max_length=100)
    director = models.CharField('Режиссер', max_length=100)
    year = models.IntegerField('Год выпуска')
    genre = models.CharField('Жанр', max_length=50)
    
    def __str__(self):
        return self.title