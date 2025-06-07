from django.db import models
from pygments.lexer import default


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview_image = models.ImageField(upload_to='blog/images/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count =  models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'Заголовок: {self.title}, опубликовано: {self.created_at}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['title']
