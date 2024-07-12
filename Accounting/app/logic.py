from django.db import transaction
from .models import BankAccount, Invoice


class InvoiceProcessor:
    @staticmethod
    def process_invoice(invoice: Invoice):
        # Calculate changes in products and accounts based on invoice items
        try:
            with transaction.atomic():

                # Update bank account balance if invoice type is 'sale' and account type is 'store'
                store_account = BankAccount.objects.get(user=invoice.user, account_type='store')
                rem_amount = invoice.remaining_amount

                if invoice.invoice_type == 'sale':
                    store_account.balance += rem_amount
                    store_account.save()
                elif invoice.invoice_type == 'purchase':
                    store_account.balance -= rem_amount
                    store_account.save()

                invoice.remaining_amount = 0
                invoice.save(update_fields=['remaining_amount'])

                # Process each invoice item
                for item in invoice.invoice_items.filter(is_submitted=False):
                    product = item.product
                    quantity = item.quantity

                    # Update product quantity based on invoice type
                    if invoice.invoice_type == 'sale':
                        product.quantity -= quantity
                    elif invoice.invoice_type == 'purchase':
                        product.quantity += quantity

                    item.is_submitted = True
                    item.save(update_fields=['is_submitted'])
                    # Save the updated product
                    product.save()

        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error processing invoice: {e}")
