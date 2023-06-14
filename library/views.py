from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .forms import ReaderForm
from .models import Book, Reader


def get_main_page(request):
    return render(request, 'main.html')


def get_new_book(request):
    return render(request, 'new_book.html')


def get_new_reader(request):
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReaderForm()
    else:
        form = ReaderForm()
    return render(request, 'new_reader.html', context={'form': form})


def get_lend_book(request):
    return render(request, 'lend_book.html')


def get_return_book(request):
    return render(request, 'return_book.html')


class BooksListView(ListView):
    model = Book
    template_name = 'list_books.html'
    context_object_name = 'books'
    # paginate_by = 3
    ordering = ['title_rus']

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
