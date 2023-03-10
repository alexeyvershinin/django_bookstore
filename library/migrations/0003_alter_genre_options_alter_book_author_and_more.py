# Generated by Django 4.1.2 on 2022-11-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_genre_alter_book_options_book_genres'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['title'], 'verbose_name': 'Жанр книги', 'verbose_name_plural': 'Жанры книг'},
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=150, verbose_name='Автор книги'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_type',
            field=models.CharField(choices=[('мягкая', 'мягкая'), ('твердая', 'твердая')], default='твердая', max_length=7, verbose_name='Тип обложки'),
        ),
    ]
