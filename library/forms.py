from django import forms
from .models import Reader


class ReaderForm(forms.ModelForm):

    class Meta:
        model = Reader
        fields = '__all__'
