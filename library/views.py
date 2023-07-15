import datetime

from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import ReaderForm, BookForm, AuthorForm, GenreForm, OrderForm, ReturnOrderForm
from .models import Book, Reader, Order, BookInstance
from .utils import save_reader_id
from django.contrib import messages


# class SearchBookView(ListView):
#     template_name = 'list_books.html'
#     context_object_name = 'books'
#
#     def get_queryset(self):
#         return Book.objects.filter(title_rus__icontains=self.request.GET.get('author_name'))
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def get_main_page(request):
    return render(request, 'main.html')


def get_new_reader(request):
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReaderForm()
    else:
        form = ReaderForm()
    return render(request, 'new_reader.html', context={'form': form})


def get_new_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            print(form.instance)
            for i in range(form.cleaned_data.get('quantity_books')):
                BookInstance.objects.create(book=form.instance)

            form = BookForm()
    else:
        form = BookForm()
    return render(request, 'new_book.html', context={'form': form})


def get_new_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            form = GenreForm()
    else:
        form = GenreForm()
    return render(request, 'new_genre.html', context={'form': form})


def get_new_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            form = AuthorForm()
    else:
        form = AuthorForm()
    return render(request, 'new_author.html', context={'form': form})


def get_new_order(request, *args, **kwargs):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            form = OrderForm()
    else:
        form = OrderForm()
    return render(request, 'new_order.html', context={'form': form})


# def create_test_order(request, **kwargs):
#     reader = kwargs.get('pk')
#     Order.objects.create(reader_id=reader)
#     return redirect('books_list_page')


def get_lend_book(request):
    return render(request, 'lend_book.html')


def get_return_book(request):
    return render(request, 'return_book.html')


# class ReaderDetailView(DetailView):
#     model = Reader
#     template_name = 'reader.html'
#     context_object_name = 'reader'


def get_reader(request, id):
    reader = Reader.objects.get(id=id)
    context = {'reader': reader}
    save_reader_id['cdi'] = id
    save_reader_id['name'] = f'{reader.surname} {reader.first_name}'
    return render(request, 'reader.html', context)


class BooksListView(ListView):
    model = Book
    template_name = 'list_books.html'
    context_object_name = 'books'
    # paginate_by = 3
    ordering = ['title_rus']

    def get_queryset(self):
        author_name = self.request.GET.get('author_name')
        if author_name == '' or author_name is None:
            return super().get_queryset()
        return Book.objects.filter(title_rus__icontains=author_name)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReadersListView(ListView):
    model = Reader
    template_name = 'list_readers.html'
    context_object_name = 'readers'
    # paginate_by = 3
    ordering = ['surname']

    def get_queryset(self):
        reader_name = self.request.GET.get('reader_name')
        if reader_name == '' or reader_name is None:
            return super().get_queryset()
        return Reader.objects.filter(surname__icontains=reader_name)


def list_books_with_id(request):
    book_name = request.GET.get('book_name')
    if book_name == '' or book_name is None:
        books = Book.objects.prefetch_related('genres', 'bookinstance_set').order_by('title_rus')
    else:
        books = Book.objects.filter(title_rus__icontains=book_name)
    return render(request, 'list_books.html', context={'books': books})


def clean_cp(request):
    """
    Очистка контекстпроцессора и редирект
    """
    save_reader_id['cdi'] = 0
    save_reader_id['name'] = ''
    current_address: str = request.META.get('HTTP_REFERER')
    if current_address[-2].isdigit():  # условие требует уточнений или регулярки
        # исключаем редирект на страницу этого же читателя
        return redirect('readers_list_page')
    return HttpResponseRedirect(current_address)


def get_list_book_instance(request, id):
    book = Book.objects.get(id=id)
    instances = book.bookinstance_set.all()
    context = {'book': book, 'instances': instances}
    return render(request, 'list_book_instance.html', context)


def get_add_to_order(request, id):
    if save_reader_id['cdi'] != 0:
        book_instance_got = BookInstance.objects.get(id=id)
        order, created = Order.objects.get_or_create(reader=Reader.objects.get(id=save_reader_id['cdi']),
                                                     order_status='active')
        # bi_in_order = order.book_instance.all()
        if order.book_instance.count() == 5:
            # print('В заказе уже 5 книг!')
            messages.add_message(request, messages.INFO, "В заказе уже 5 книг!")
            return redirect('list_books_with_id')
        for b in order.book_instance.all():
            if b.book_id == book_instance_got.book_id:
                # print('Другой экземпляр данной книги уже добавлен в заказ.')
                messages.add_message(request, messages.INFO, "Другой экземпляр данной книги уже добавлен в заказ")
                return redirect('list_books_with_id')
        order.book_instance.add(book_instance_got)
        book_instance_got.status = 'c'
        book_instance_got.save()
        order.save()
    return redirect('list_books_with_id')


def check_order(request):
    # проверям, выбран ли читатель, иначе редирект на главную
    if save_reader_id['cdi'] != 0:
        order, created = Order.objects.get_or_create(reader=Reader.objects.get(id=save_reader_id['cdi']),
                                                     order_status='active')
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                # сохраняю заказ, переводя статус экземпляров книг в "r - В аренде"
                for book in order.book_instance.all():
                    book.status = 'r'
                    book.save()
                form.save()
                form = OrderForm(instance=order)
        else:
            form = OrderForm(instance=order)
        context = {'order': order, 'form': form}
        return render(request, 'check_order.html', context)
    else:
        return redirect('main_page')


def delete_from_order(request, id):
    if save_reader_id['cdi'] != 0:
        order = Order.objects.get(reader=Reader.objects.get(id=save_reader_id['cdi']), order_status='active')
        book_instance_got = BookInstance.objects.get(id=id)
        order.book_instance.remove(book_instance_got)
        book_instance_got.status = 'f'
        book_instance_got.save()
        order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def return_order(request):
    # проверям, выбран ли читатель, иначе редирект на главную
    if save_reader_id['cdi'] != 0:
        order = Order.objects.get(reader=Reader.objects.get(id=save_reader_id['cdi']), order_status='active')
        order.return_date = datetime.date.today()
        # if order.return_date - order.order_time > 30:
        print(order.return_date - order.order_time < datetime.timedelta(days=30))
        order.save()
        if request.method == 'POST':
            form = ReturnOrderForm(request.POST, instance=order)
            if form.is_valid():
                # сохраняю заказ, переводя статус экземпляров книг в "f - Свободна"
                for book in order.book_instance.all():
                    book.status = 'f'
                    order.book_instance.remove(book)
                    book.save()
                form.save()
                order.order_status = 'finished'
                order.save()
                return redirect('main_page')
        else:
            form = ReturnOrderForm(instance=order)
        context = {'order': order, 'form': form}
        return render(request, 'return_order.html', context)
    else:
        return redirect('main_page')

