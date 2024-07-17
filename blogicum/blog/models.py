"""Модуль для создания и описания моделей проекта."""

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class CommonModel(models.Model):
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
        """Класс с определением метаданных модели CommonModel."""

        abstract = True


class Post(CommonModel):
    """Класс, с описанием модели Post."""

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        'Изображение', upload_to='post_images', blank=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        # Автотесты не пропустили оформление текста
        # через тройные одиночные кавычки.
        help_text=(
            'Если установить дату и время в будущем — '
            + 'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories'
    )

    class Meta:
        """Класс с определением метаданных модели Post."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.title

    def comment_count(self):
        """Считает кол-во комментариев поста."""
        return Comment.objects.filter(post=self).count()


class Category(CommonModel):
    """Класс, с описанием модели Category."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        # Автотесты не пропустили оформление текста
        # через тройные одиночные кавычки.
        help_text=(
            'Идентификатор страницы для URL; '
            + 'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        """Класс с определением метаданных модели Category."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.title


class Location(CommonModel):
    """Класс, с описанием модели Location."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        """Класс с определением метаданных модели Location."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Выводит читаемые названия объектов."""
        return self.name


class Comment(models.Model):
    """Класс с описанием модели комментария."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Класс с определением метаданных модели Comment."""

        ordering = ('created_at',)
