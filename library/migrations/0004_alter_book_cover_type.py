# Generated by Django 4.1.2 on 2022-11-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_genre_options_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_type',
            field=models.CharField(choices=[('мягкая', 'мягкая'), ('твердая', 'твердая')], default='мягкая', max_length=7, verbose_name='Тип обложки'),
        ),
    ]
