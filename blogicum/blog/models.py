"""Модуль для создания и описания моделей проекта."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Произвольное значение для усечения длины
# выводимых наименований и оглавлений объектов моделей.
OBJECT_NAME_MAX_LENGHT = 32


class PubCheckAndCreationTimeModel(models.Model):
    """Класс, с описанием общих для моделей атрибутов."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(PubCheckAndCreationTimeModel):
    """Класс, с описанием модели категории."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.title[:OBJECT_NAME_MAX_LENGHT]


class Location(PubCheckAndCreationTimeModel):
    """Класс, с описанием модели локации."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.name[:OBJECT_NAME_MAX_LENGHT]


class Post(PubCheckAndCreationTimeModel):
    """Класс, с описанием модели поста."""

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        'Изображение', upload_to='post_images', blank=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.title[:OBJECT_NAME_MAX_LENGHT]


class Comment(models.Model):
    """Класс с описанием модели комментария."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='пост',
        related_name='comments'
    )
    created_at = models.DateTimeField(
        verbose_name='опубликован', auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return (
            f'Пост: {self.post.title[:OBJECT_NAME_MAX_LENGHT]}. '
            f'Текст: {self.text[:OBJECT_NAME_MAX_LENGHT]}'
        )
