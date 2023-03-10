# Generated by Django 4.1.2 on 2022-12-05 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pos_order',
            options={'verbose_name': 'Позицию в заказе', 'verbose_name_plural': 'Позиции в заказе'},
        ),
        migrations.AlterField(
            model_name='pos_order',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order', verbose_name='Заказ'),
        ),
    ]
