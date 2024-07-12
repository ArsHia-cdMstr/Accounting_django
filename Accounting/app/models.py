from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    journal_list = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    trans_name = models.CharField(max_length=30)
    trans_type = models.CharField(max_length=3)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.trans_name


class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('checking', 'Checking'),
        ('loan', 'Loan'),
        ('store', 'Store')
    )

    bank_name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            self.account_number = self.id + 1000
            self.save(update_fields=['account_number'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    INVOICE_TYPES = (
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    invoice_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            self.invoice_number = self.id + 1000
            self.save(update_fields=['invoice_number'])
        super().save(*args, **kwargs)

    def update_total_amount(self):
        total = self.invoice_items.aggregate(total=Sum('amount'))['total']
        self.total_amount = total if total else 0
        self.save(update_fields=['total_amount'])

    def update_remaining_amount(self, amount):
        self.remaining_amount = amount
        self.save(update_fields=['remaining_amount'])

    def __str__(self):
        return f"{self.customer.name} - {self.invoice_type} - {self.date}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_submitted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.amount = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.invoice.update_total_amount()
        self.invoice.update_remaining_amount(amount=self.amount)


    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.bank_account} - {self.amount} - {self.date}"
