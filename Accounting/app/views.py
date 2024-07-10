from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import DeleteView

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BankAccount, Customer, Product, Invoice, InvoiceItem, Check, Portfolio


class PortfolioCreate(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/portfolio_create_form.html')

    def post(self, request):
        user = User.objects.get(username=request.user)
        pfl_name = request.POST.get('portfolio_name')
        user.portfolio_set.create(name=pfl_name)
        my_object = user.portfolio_set.get(name=pfl_name).id
        return redirect('pfl-detail', my_object)


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    template = 'app/portfolio_confirm_delete.html'
    model = Portfolio
    success_url = reverse_lazy('pfl-list')


class PortfolioList(LoginRequiredMixin, View):
    def get(self, request):
        account = User.objects.get(username=request.user)
        context = {'user': account}
        return render(request, 'app/home.html', context)


class UserLogin(LoginView):
    template_name = 'app/signin.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pfl-list')


class UserSignup(FormView):
    template_name = 'app/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pfl-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignup, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pfl-list')
        return super(UserSignup, self).get(*args, **kwargs)


class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'app/bankaccount_list.html'

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)


class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    fields = ['account_type', 'balance']
    template_name = 'app/bankaccount_form.html'
    success_url = reverse_lazy('bankaccount-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'app/customer_list.html'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['name', 'email']
    template_name = 'app/customer_form.html'
    success_url = reverse_lazy('customer-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'app/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'quantity']
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'app/invoice_list.html'
    context_object_name = 'invoices'  # نام متغیری که در template قابل دسترس است

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)
class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = ['invoice_type', 'customer']
    template_name = 'app/invoice_form.html'
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvoiceItemCreateView(LoginRequiredMixin, CreateView):
    model = InvoiceItem
    fields = ['invoice', 'product', 'quantity']
    template_name = 'app/invoiceitem_form.html'
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CheckListView(LoginRequiredMixin, ListView):
    model = Check
    template_name = 'app/check_list.html'

    def get_queryset(self):
        return Check.objects.filter(user=self.request.user)


class CheckCreateView(LoginRequiredMixin, CreateView):
    model = Check
    fields = ['bank_account', 'customer', 'amount', 'date']
    template_name = 'app/check_form.html'
    success_url = reverse_lazy('check-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
