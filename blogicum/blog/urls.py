"""Модуль маршрутизации приложения blog."""

from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPosts.as_view(),
        name='category_posts'
    ),
    path(
        'profile/<str:username>/',
        views.UserProfile.as_view(),
        name='profile'
    ),
    path(
        'edit-profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'posts/<int:post>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post>/edit_comment/<int:comment_id>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post>/delete_comment/<int:comment_id>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),

]
