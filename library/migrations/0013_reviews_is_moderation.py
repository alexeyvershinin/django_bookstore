# Generated by Django 4.1.2 on 2022-12-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_alter_book_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='is_moderation',
            field=models.BooleanField(default=False),
        ),
    ]
