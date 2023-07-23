from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, TextInput
import re

from .models import Reader, Book, Genre, Author, Order


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'

    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if not re.fullmatch(r'[A-Za-z]{2}[0-9]{7}', passport_number):
            raise ValidationError("Не правильный номер паспорта")
        return passport_number



class BookForm(forms.ModelForm):
    quantity_books = forms.IntegerField(label='Количество экземпляров')

    class Meta:
        model = Book
        fields = '__all__'
        localized_fields = ('date_reg',)
        widgets = {
            'title_rus': TextInput(attrs={}),

        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_time', 'return_date']


class ReturnOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
