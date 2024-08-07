from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


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
        initial_balance = None
        if self.pk is not None:
            initial_balance = BankAccount.objects.get(pk=self.pk).balance

        super().save(*args, **kwargs)

        if self.pk is None:
            self.account_number = self.id + 1000
            super().save(update_fields=['account_number'])

        balance_change = self.balance - initial_balance if initial_balance is not None else self.balance
        AccountHistory.objects.create(
            mother_account=self,
            balance_change=balance_change,
            remaining_balance=self.balance
        )

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"


class AccountHistory(models.Model):
    mother_account = models.ForeignKey(BankAccount, related_name="account_history", on_delete=models.CASCADE)
    balance_change = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of {self.mother_account} changed on {self.date_changed}"


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
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update existing product
            old_product = Product.objects.get(pk=self.pk)
            quantity_change = self.quantity - old_product.quantity
            if quantity_change != 0:
                ProductHistory.objects.create(
                    product=self,
                    quantity_change=quantity_change,
                    remaining_quantity=self.quantity,
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductHistory(models.Model):
    product = models.ForeignKey(Product, related_name="product_history", on_delete=models.CASCADE, null=True, blank=True)
    quantity_change = models.IntegerField(null=True, blank=True)
    remaining_quantity = models.IntegerField(null=True, blank=True)
    date_changed = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"History of {self.product} changed on {self.date_changed}"


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


#
#
# class InvoiceHistory(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#
#     # Add more fields as needed for history tracking
#
#     def __str__(self):
#         return f"History of {self.invoice} created on {self.date_created}"


class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.bank_account} - {self.amount} - {self.date}"


class Transference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bank_account} - {self.amount} - {self.date}"
