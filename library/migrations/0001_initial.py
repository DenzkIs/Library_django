# Generated by Django 4.2.1 on 2023-06-09 15:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Author name')),
                ('foto', models.ImageField(default='images/authors/author_default.png', upload_to='images/authors', verbose_name="Author's foto")),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_rus', models.CharField(max_length=255, verbose_name='Russian title')),
                ('title_original', models.CharField(blank=True, max_length=255, verbose_name='Original title')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Cost (BYN)')),
                ('quantity', models.IntegerField(default=0, verbose_name='Number of books')),
                ('rent_day', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Rental per day (BYN)')),
                ('year', models.IntegerField(blank=True, verbose_name='The year of published')),
                ('date_reg', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of registration')),
                ('page', models.IntegerField(blank=True, verbose_name='Number of pages')),
                ('id_author', models.ManyToManyField(to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Genre name')),
            ],
        ),
        migrations.CreateModel(
            name='BookCover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(default='images/covers/cover_default.jpg', upload_to='images/covers', verbose_name="Cover's foto")),
                ('id_book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='id_book_cover',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.bookcover'),
        ),
        migrations.AddField(
            model_name='book',
            name='id_genre',
            field=models.ManyToManyField(to='library.genre'),
        ),
    ]
