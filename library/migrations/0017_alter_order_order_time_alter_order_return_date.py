# Generated by Django 4.2.1 on 2023-07-15 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_remove_book_quantity_alter_order_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 13, 0, 15, 47184), verbose_name='Время заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 14, 13, 0, 15, 47184), verbose_name='Дата возврата'),
        ),
    ]
