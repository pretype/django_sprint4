"""Модуль, с определением форм приложения blog."""

from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    """Класс формы поста."""

    class Meta:
        """Класс с определением метаданных формы поста."""

        model = Post
        exclude = ('author', )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class ProfileChangeForm(forms.ModelForm):
    """Класс формы для редактирования профиля."""

    class Meta:
        """Класс с определением метаданных формы ред. профиля."""

        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class CommentForm(forms.ModelForm):
    """Класс формы комментария."""

    class Meta:
        """Класс с определением метаданных формы комментария."""

        model = Comment
        fields = ('text',)
