from django.urls import path

from .views import *

urlpatterns = [
    path('main/', get_main_page, name='main_page'),
    path('new_book/', get_new_book, name='new_book_page'),
    path('new_reader/', get_new_reader, name='new_reader_page'),
    path('lend_book/', get_lend_book, name='lend_book_page'),
    path('return_book/', get_return_book, name='return_book_page'),
    path('book_list/', BooksListView.as_view(), name='book_list_page'),

]