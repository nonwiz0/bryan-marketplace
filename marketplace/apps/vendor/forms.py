from django.forms import ModelForm, fields

from apps.product.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']