# Generated by Django 3.2.16 on 2024-07-21 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20240721_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='\n            Идентификатор страницы для URL;\n            разрешены символы латиницы, цифры, дефис и подчёркивание.\n        ', unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(help_text='\n            Если установить дату и время в будущем —\n            можно делать отложенные публикации.\n        ', verbose_name='Дата и время публикации'),
        ),
    ]
