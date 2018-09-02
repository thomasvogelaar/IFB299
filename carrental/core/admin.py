from django.contrib import admin
from .models import Car, Customer, Store, Transaction

admin.site.register(Car)
admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Transaction)
# Register your models here.
