from django.contrib import admin
from .models import *

import json
from django.contrib import admin

# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)