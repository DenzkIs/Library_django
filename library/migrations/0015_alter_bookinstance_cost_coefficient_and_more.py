# Generated by Django 4.2.1 on 2023-07-02 14:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_bookinstance_cost_coefficient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='cost_coefficient',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=3, verbose_name='Коэффицент стоимости'),
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 17, 43, 28, 491174), verbose_name='Дата возврата'),
        ),
    ]