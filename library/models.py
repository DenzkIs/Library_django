from django.utils import timezone
from django.db import models
import datetime
import random
from decimal import Decimal


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО автора')
    foto = models.ImageField(upload_to='images/authors', verbose_name="Фото автора",
                             default='images/authors/author_default.png')

    def __str__(self):
        return f"{self.id}: {self.name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр')

    def __str__(self):
        return self.name


class Book(models.Model):
    title_rus = models.CharField(max_length=255, verbose_name='Русское наименование')
    title_original = models.CharField(max_length=255, verbose_name='Оригинальное наименование', blank=True)
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    cost = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='Стоимость книги (BYN)')
    authors = models.ManyToManyField(Author, verbose_name='Авторы')
    rent_day = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость аренды (BYN)')
    year = models.IntegerField(blank=True, default=0, verbose_name='Год издания')
    date_reg = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    pages = models.IntegerField(blank=True, default=0, verbose_name='Количество страниц')

    def __str__(self):
        return f'{self.id}: {self.title_rus}'

    @property
    def quantity_free(self):
        total_free = 0
        for b in self.bookinstance_set.all():
            if b.status == 'f':
                total_free += 1
        return total_free
        # return self.bookinstance_set.filter(status='f').count()

    @property
    def total_quantity(self):
        return self.bookinstance_set.count()

    @property
    def book_genres(self):
        list_genres = []
        for genre in self.genres.all():
            list_genres.append(genre.name)
        str_genres = ', '.join(list_genres)
        return str_genres.lower()


class BookInstance(models.Model):
    STATUS_CHOICES = (
        ('f', 'Свободная'),
        ('r', 'В аренде'),
        ('c', 'Выбрана для заказа'),
        ('m', 'На обслуживании'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='f')
    cover_foto = models.ImageField(upload_to='images/covers', verbose_name="Фото обложки",
                                   default='images/covers/cover_default.jpg')
    cost_coefficient = models.DecimalField(max_digits=3, decimal_places=2, default=1,
                                           verbose_name="Коэффицент стоимости")

    @property
    def cost_with_coefficient(self):
        return self.cost_coefficient * self.book.rent_day

    def __str__(self):
        return f'{self.id}: {self.book.title_rus} - {self.get_status_display()}'


class Reader(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, default='')
    passport_number = models.CharField(max_length=9, null=True, blank=True, unique=True)
    birthday = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.birthday}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('finished', 'Окончен'),
        ('delayed', 'Задерживается'),
        ('active', 'У пользователя'),
        ('fills_up', 'Наполняется'),
    )
    reader = models.ForeignKey('Reader', on_delete=models.CASCADE, verbose_name='Читатель', null=True)
    book_instance = models.ManyToManyField('BookInstance', verbose_name='Экземпляр книги', null=True)
    order_time = models.DateField(default=datetime.date.today(), verbose_name='Дата заказа')
    return_date = models.DateField(verbose_name='Дата возврата',
                                       default=datetime.date.today() + datetime.timedelta(days=30))
    order_status = models.CharField(max_length=8, default='fills_up', choices=STATUS_CHOICES,
                                    verbose_name='Статус заказа')
    penalty_for_delay = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Пеня за задержку')
    damage_penalty = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Штраф за повреждения')
    finish_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                      verbose_name='Итоговая стоимость заказа')

    @property
    def rental_days(self):
        print(self.return_date, 'дата возврата')
        print(self.order_time, 'дата заказа')
        return round((self.return_date - self.order_time).total_seconds() / 60 / 60 / 24)


    @property
    def sum_cost(self):
        total = 0
        discount = 1
        quantity = self.book_instance.count()
        if 2 < quantity < 5:
            discount = 0.90
        elif quantity == 5:
            discount = 0.85
        for book in self.book_instance.all():
            total += book.cost_with_coefficient
        return (total * self.rental_days * Decimal(discount)).quantize(Decimal("1.00"))

    def __str__(self):
        return f'Заказ №{self.id} - {self.reader} - {self.get_order_status_display()}'

# def save(self, *args, **kwargs):
#     self.return_date = self.order_time + datetime.timedelta(days=30)
#     super().save(*args, **kwargs)
