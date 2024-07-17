"""Модуль, с определением функций-обработчиков приложения blog."""

from datetime import datetime

from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView, DetailView, DeleteView, ListView, CreateView
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Category, Comment, Post, User
from .forms import ProfileChangeForm, PostForm, CommentForm


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс проверки авторства пользователя."""

    def test_func(self):
        """Проверяет авторство текущего пользователя."""
        object = self.get_object()
        return object.author == self.request.user


class PostsListMixin:
    """Класс с общими атрибутами для коллекций постов."""

    model = Post
    ordering = 'pub_date'
    paginate_by = 10


class CommentMixin:
    """Класс с общими атрибутами для комментариев."""

    model = Comment
    form_class = CommentForm


def default_fields(model_objects, now):
    """Содержит общие стандартные значения вью полей."""
    return model_objects.filter(
        pub_date__date__lte=now,
        is_published=True,
        category__is_published=True
    )


class Index(PostsListMixin, ListView):
    """Класс с обработкой главной страницы."""

    template_name = 'blog/index.html'

    def get_queryset(self):
        """Получает отфильтрованный список постов."""
        now = timezone.now()
        post_list = default_fields(Post.objects, now)
        return post_list


class PostDetailView(DetailView):
    """Класс с обработкой страницы определенного поста."""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        """Описание словаря контекста поста."""
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        if (
            (obj.pub_date <= timezone.now()
             and obj.is_published
             and obj.category.is_published)
            or obj.author == self.request.user
        ):
            return context
        else:
            raise Http404()


class CategoryPosts(PostsListMixin, ListView):
    """Класс с обработкой страницы категории."""

    template_name = 'blog/category.html'

    def get_queryset(self):
        """Получает отфильтрованный список постов опр. категории."""
        now = timezone.now()
        category = get_object_or_404(
            Category.objects, slug=self.kwargs['category_slug'])
        cat_posts = category.categories.filter(category=category)
        posts = default_fields(cat_posts, now)
        if category.is_published:
            return posts
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Описание словаря контекста категории."""
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category.objects, slug=self.kwargs['category_slug'])
        return context


class UserProfile(PostsListMixin, ListView):
    """Класс с обработкой страницы профиля."""

    template_name = 'blog/profile.html'

    def get_queryset(self):
        """Получает отфильтрованный список постов опр. пользователя."""
        user = get_object_or_404(
            User.objects, username=self.kwargs['username']
        )
        user_id = user.id
        now = datetime.now()
        if user == self.request.user:
            posts = Post.objects.filter(author=user_id)
        else:
            posts = default_fields(
                Post.objects.filter(
                    author=user_id
                ),
                now
            )
        return posts

    def get_context_data(self, **kwargs):
        """Описание словаря контекста профиля."""
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(
            User.objects, username=self.kwargs['username']
        )
        context['profile'] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Класс с обработкой страницы изменения профиля."""

    model = User
    form_class = ProfileChangeForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    """Класс с обработкой создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        """Перенаправляет пользователя после успешного создания поста."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        """Валидация формы."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Класс с обработкой редактирования поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        """Перенаправляет пользователя после успешного редактирования поста."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def handle_no_permission(self):
        """Перенаправляет пользователя без доступа к редактированию поста."""
        return redirect('blog:post_detail', pk=self.kwargs['pk'])


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Класс с обработкой удаления поста."""

    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        """Перенаправляет пользователя после успешного удаления поста."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """Класс с обработкой создания комментария."""

    post_obj = None

    def dispatch(self, request, *args, **kwargs):
        """Получает pk текущего поста."""
        self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Валидация формы."""
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляет пользователя после добавления комментария."""
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.post_obj.pk}
        )


class EditCommentView(OnlyAuthorMixin, CommentMixin, UpdateView):
    """Класс с обработкой редактирования комментария."""

    template_name = 'blog/comment.html'

    def get_object(self):
        """Получает редактируемый пользователем комментарий."""
        return get_object_or_404(Comment.objects, pk=self.kwargs['comment_id'])

    def get_success_url(self):
        """Перенаправляет пользователя после редактирования комментария."""
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class DeleteCommentView(OnlyAuthorMixin, CommentMixin, DeleteView):
    """Класс с обработкой удаления комментария."""

    template_name = 'blog/comment.html'

    def get_object(self):
        """Получает комментарий редактируемый пользователем."""
        return get_object_or_404(Comment.objects, pk=self.kwargs['comment_id'])

    def get_success_url(self):
        """Перенаправляет пользователя после удаления комментария."""
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )
