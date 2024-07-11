from django import forms
from .models import BankAccount


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_type', 'balance', 'bank_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BankAccountForm, self).__init__(*args, **kwargs)

    def clean_account_type(self):
        account_type = self.cleaned_data.get('account_type')

        if account_type == 'store':
            if BankAccount.objects.filter(user=self.user, account_type='store').exists():
                raise forms.ValidationError('You already have an account with type "store".')
        return account_type

