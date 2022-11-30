from .models import * 
from django import forms
import django_filters




class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['name', 'drug_class', 'price']