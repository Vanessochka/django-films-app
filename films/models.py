from django.db import models

class Film(models.Model):
    title = models.CharField("Название фильма", max_length=100, unique=True)
    director = models.CharField("Режиссер", max_length=100)
    year = models.IntegerField("Год выпуска")
    genre = models.CharField("Жанр", max_length=50)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
