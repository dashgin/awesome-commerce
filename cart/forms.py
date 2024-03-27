from django import forms
from .models import Product


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=100)
    product_id = forms.IntegerField()
    id_by_size = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        id_by_size = cleaned_data.get("id_by_size")
        if id_by_size:
            product_id = id_by_size
        else:
            product_id = cleaned_data["product_id"]

        quantity = cleaned_data["quantity"]
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise forms.ValidationError("Product not found")
        if product.quantity < quantity:
            raise forms.ValidationError("Not enough stock")
        cleaned_data["product"] = product
        return cleaned_data


class RemoveFromCartForm(forms.Form):
    product_id = forms.IntegerField()
