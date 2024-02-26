from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'author', 'description', 'image', 'category', 'price', 'amount', 'phone_number',
                  'additional_contact']
