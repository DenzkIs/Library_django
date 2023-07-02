# Generated by Django 4.2.1 on 2023-07-02 19:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_bookinstance_cost_coefficient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 22, 41, 27, 893612), verbose_name='Дата возврата'),
        ),
    ]
