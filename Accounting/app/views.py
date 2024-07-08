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
