from django.contrib import admin
from .models import Portfolio, BankAccount, Customer, Product, Invoice, InvoiceItem, Check, Transference

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(BankAccount)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Check)
admin.site.register(Transference)
