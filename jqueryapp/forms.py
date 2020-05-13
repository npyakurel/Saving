from django import forms
from .models import *


class CartForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


