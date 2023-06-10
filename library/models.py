from django.utils import timezone

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
    id_genre = models.ManyToManyField(Genre)
    cost = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='Cost (BYN)')
    quantity = models.IntegerField(default=0, verbose_name='Number of books')
    id_author = models.ManyToManyField(Author)
    rent_day = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Rental per day (BYN)')
    year = models.IntegerField(blank=True, default=0, verbose_name='The year of published')
    date_reg = models.DateTimeField(default=timezone.now, verbose_name='Date of registration')
    page = models.IntegerField(blank=True, default=0, verbose_name='Number of pages')

    def __str__(self):
        return f'{self.id}: {self.title_rus}'


    @property
    def quantity_free(self):
        return self.bookinstance_set.filter(status='f').count()

    @property
    def book_genres(self):
        list_genres = []
        for genre in self.id_genre.all():
            list_genres.append(genre.name)
        str_genres = ', '.join(list_genres)
        return str_genres.lower()



# class BookCover(models.Model):
#     id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     foto = models.ImageField(upload_to='images/covers', verbose_name="Cover's foto",
#                              default='images/covers/cover_default.jpg')
#
#     def __str__(self):
#         return 'Cover for book'

class BookInstance(models.Model):

    STATUS_CHOICES = (
        ('f', 'Free'),
        ('r', 'Rented'),
        ('m', 'Maintenance'),
    )
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='f')

    def __str__(self):
        return f'{self.id}: {self.id_book.title_rus} - {self.get_status_display()}'


class Reader(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, default='')
    passport_number = models.CharField(max_length=9, blank=True, default='', unique=True)
    birthday = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    # сделать ввод адреса подробнее!
    address = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.birthday}'
