# app/urls.py

from django.urls import path
from .views import (
    BankAccountListView, BankAccountCreateView,
    CustomerListView, CustomerCreateView,
    ProductListView, ProductCreateView,
    InvoiceListView, InvoiceCreateView, InvoiceDetailView, InvoiceItemCreateView,
    CheckListView, CheckCreateView,
    UserSignup, UserLogin

)
from .views import UserSignup, UserLogin, PortfolioList, PortfolioCreate, PortfolioDelete
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', PortfolioList.as_view(), name='pfl-list'),
    path('pfl-create/', PortfolioCreate.as_view(), name='pfl-create'),
    path('pfl-delete/pk=<int:pk>', PortfolioDelete.as_view(), name='pfl-delete'),


    path('bankaccounts/', BankAccountListView.as_view(), name='bankaccount-list'),
    path('bankaccounts/create/', BankAccountCreateView.as_view(), name='bankaccount-create'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/items/create/', InvoiceItemCreateView.as_view(), name='invoiceitem-create'),
    path('checks/', CheckListView.as_view(), name='check-list'),
    path('checks/create/', CheckCreateView.as_view(), name='check-create'),
]
