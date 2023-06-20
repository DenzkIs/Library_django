# Generated by Django 4.2.1 on 2023-06-20 19:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_remove_order_book_instance_alter_order_return_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='book_instance',
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 20, 22, 32, 51, 387625), verbose_name='Дата возврата'),
        ),
        migrations.AddField(
            model_name='order',
            name='book_instance',
            field=models.ManyToManyField(null=True, to='library.bookinstance', verbose_name='Экземпляр книги'),
        ),
    ]
