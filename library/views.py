from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import ReaderForm, BookForm, AuthorForm, GenreForm, OrderForm
from .models import Book, Reader, Order


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
            form.save()
            form = BookForm()
    else:
        form = BookForm()
    return render(request, 'new_book.html', context={'form': form})


def get_new_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        print(request.POST)
        print(form)
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


def create_test_order(request, **kwargs):
    reader = kwargs.get('pk')
    Order.objects.create(reader_id=reader)
    return redirect('books_list_page')


def get_lend_book(request):
    return render(request, 'lend_book.html')


def get_return_book(request):
    return render(request, 'return_book.html')


class ReaderDetailView(DetailView):
    model = Reader
    template_name = 'reader.html'
    context_object_name = 'reader'


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

    # def get_context_data(self, **kwargs):
    #     context = super(BooksListView, self).get_context_data(**kwargs)
    #     return context
    # book.bookinstance_set.filter(status='f').count()


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
