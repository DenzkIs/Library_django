from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Author name')
    foto = models.ImageField(upload_to='images/authors', verbose_name="Author's foto",
                             default='images/authors/author_default.png')

    def __str__(self):
        return f"{self.id}: {self.name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Genre name')

    def __str__(self):
        return self.name


class Book(models.Model):
    title_rus = models.CharField(max_length=255, verbose_name='Russian title')
    title_original = models.CharField(max_length=255, verbose_name='Original title', blank=True)
    genre = models.ManyToManyField(Genre)
    cost = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='Cost (BYN)')
    quantity = models.IntegerField(default=0, verbose_name='Number of books')
    author = models.ManyToManyField(Author)
    rent_day = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Rental per day (BYN)')
    year = models.IntegerField(blank=True, verbose_name='The year of published')
    date_reg = models.DateTimeField(auto_now_add=True, verbose_name='Date of registration')
    page = models.IntegerField(blank=True, verbose_name='Number of pages')

    def __str__(self):
        return f'{self.id}: {self.title_rus}'


class BookCover(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='images/covers', verbose_name="Cover's foto",
                             default='images/covers/cover_default.jpg')

    def __str__(self):
        return 'Cover for book'
