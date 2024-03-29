# Generated by Django 4.2.1 on 2023-07-19 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_alter_order_order_status_alter_order_order_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateField(default=datetime.date(2023, 7, 19), verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateField(default=datetime.date(2023, 8, 18), verbose_name='Дата возврата'),
        ),
    ]
