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
]
