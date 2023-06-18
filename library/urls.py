from django.urls import path

from .views import *

urlpatterns = [
    path('main/', get_main_page, name='main_page'),
    path('new_book/', get_new_book, name='new_book_page'),
    path('new_reader/', get_new_reader, name='new_reader_page'),
    path('new_order/', get_new_order, name='new_order_page'),
    path('lend_book/', get_lend_book, name='lend_book_page'),
    path('return_book/', get_return_book, name='return_book_page'),
    path('books_list/', BooksListView.as_view(), name='books_list_page'),
    path('readers_list/', ReadersListView.as_view(), name='readers_list_page'),
    path('new_genre/', get_new_genre, name='new_genre_page'),
    path('create_test_order/', create_test_order, name='create_test_order'),
    path('new_author/', get_new_author, name='new_author_page'),
    path('reader/<int:pk>/', ReaderDetailView.as_view(), name='reader_detail'),

]
