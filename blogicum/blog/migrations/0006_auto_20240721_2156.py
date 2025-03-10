# Generated by Django 3.2.16 on 2024-07-21 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('title',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('name',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='\n            Идентификатор страницы для URL; \n            разрешены символы латиницы, цифры, дефис и подчёркивание.\n        ', unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='опубликован'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='пост'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.location', verbose_name='Местоположение'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(help_text='\n            Если установить дату и время в будущем — \n            можно делать отложенные публикации.\n        ', verbose_name='Дата и время публикации'),
        ),
    ]
