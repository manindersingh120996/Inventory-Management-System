from django.contrib import admin
from .models import product
from .models import category, cart, order
# Register your models here.

admin.site.register(product)
admin.site.register(category)
admin.site.register(cart)
admin.site.register(order)
