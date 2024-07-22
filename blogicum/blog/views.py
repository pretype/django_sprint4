"""Модуль, с определением функций-обработчиков приложения blog."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, ProfileChangeForm
from .models import Category, Comment, Post, User


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс проверки авторства пользователя."""

    def test_func(self):
        """Проверяет авторство текущего пользователя."""
        return self.get_object().author == self.request.user


class PostsListMixin:
    """Класс с общими атрибутами для коллекций постов."""

    model = Post
    paginate_by = 10


class CommentMixin:
    """Класс с общими атрибутами для комментариев."""

    model = Comment
    form_class = CommentForm


class PostCreateMutateMixin:
    """Класс с общими атрибутами для создания и изменения поста."""

    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        """Перенаправляет пользователя после успешного удаления поста."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentDelEditMixin:
    """Класс с общими атрибутами для удаления и изменения комментария."""

    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        """Перенаправляет пользователя после удаления комментария."""
        return reverse(
            'blog:post_detail',
            kwargs={'post': self.kwargs['post']}
        )


def posts_default_fields(posts):
    """Содержит стандартные сортировку, фильтры и подсчет для постов."""
    return posts.filter(
        pub_date__date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class Index(PostsListMixin, ListView):
    """Класс с обработкой главной страницы."""

    template_name = 'blog/index.html'
    queryset = posts_default_fields(Post.objects)


class PostDetailView(DetailView):
    """Класс с обработкой страницы определенного поста."""

    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        """Получает текущий пост или ошибку '404'."""
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post']
        )
        if post.author == self.request.user:
            return post
        else:
            return get_object_or_404(
                posts_default_fields(Post.objects),
                pk=self.kwargs['post']
            )

    def get_context_data(self, **kwargs):
        """Описание словаря контекста поста."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CategoryPosts(PostsListMixin, ListView):
    """Класс с обработкой страницы категории."""

    template_name = 'blog/category.html'

    def get_category(self):
        """Получает опубликованную категорию или ошибку '404'."""
        return get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug']
        )

    def get_queryset(self):
        """Получает отфильтрованный список постов опр. категории."""
        return posts_default_fields(self.get_category().posts)

    def get_context_data(self, **kwargs):
        """Описание словаря контекста категории."""
        return super().get_context_data(**kwargs, category=self.get_category())


class UserProfile(PostsListMixin, ListView):
    """Класс с обработкой страницы профиля."""

    template_name = 'blog/profile.html'

    def get_author(self):
        """Получает автора или ошибку "404"."""
        return get_object_or_404(
            User.objects, username=self.kwargs['username']
        )

    def get_queryset(self):
        """Получает отфильтрованный список постов опр. пользователя."""
        author = self.get_author()
        if author == self.request.user:
            posts = (author.posts.all()
                     .annotate(comment_count=Count('comments'))
                     .order_by('-pub_date')
                     )
        else:
            posts = posts_default_fields(
                author.posts.all()
            )
        return posts

    def get_context_data(self, **kwargs):
        """Описание словаря контекста профиля."""
        return super().get_context_data(**kwargs, profile=self.get_author())


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Класс с обработкой страницы изменения профиля."""

    model = User
    form_class = ProfileChangeForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user


class PostCreateView(LoginRequiredMixin, PostCreateMutateMixin, CreateView):
    """Класс с обработкой создания поста."""

    form_class = PostForm

    def form_valid(self, form):
        """Валидация формы."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, PostCreateMutateMixin, UpdateView):
    """Класс с обработкой редактирования поста."""

    form_class = PostForm

    def get_object(self):
        """Получает текущий пост."""
        return get_object_or_404(Post, pk=self.kwargs['post'])

    def handle_no_permission(self):
        """Перенаправляет пользователя без доступа к редактированию поста."""
        return redirect('blog:post_detail', self.kwargs['post'])


class PostDeleteView(OnlyAuthorMixin, PostCreateMutateMixin, DeleteView):
    """Класс с обработкой удаления поста."""

    def get_object(self):
        """Получает текущий пост."""
        return get_object_or_404(Post, pk=self.kwargs['post'])


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """Класс с обработкой создания комментария."""

    def get_object(self):
        """Получает текущий пост."""
        return get_object_or_404(
            Post,
            pk=self.kwargs['post']
        )

    def form_valid(self, form):
        """Валидация формы."""
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляет пользователя после добавления комментария."""
        return reverse(
            'blog:post_detail',
            kwargs={'post': self.kwargs['post']}
        )


class EditCommentView(
    OnlyAuthorMixin, CommentMixin, CommentDelEditMixin, UpdateView
):
    """Класс с обработкой редактирования комментария."""


class DeleteCommentView(
    OnlyAuthorMixin, CommentMixin, CommentDelEditMixin, DeleteView
):
    """Класс с обработкой удаления комментария."""
