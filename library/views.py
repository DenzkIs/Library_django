from django.shortcuts import render


def get_main_page(request):
    return render(request, 'main.html')


def get_new_book(request):
    return render(request, 'new_book.html')


def get_new_reader(request):
    return render(request, 'new_reader.html')


def get_lend_book(request):
    return render(request, 'lend_book.html')


def get_return_book(request):
    return render(request, 'return_book.html')
