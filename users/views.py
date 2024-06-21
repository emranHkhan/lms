from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from . import forms
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from django.views.generic import ListView
from .models import Borrow, UserAccount
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully!')
        return super().form_valid(form)
    

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

class DepositView(LoginRequiredMixin, FormView):
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully. Check you email.'
        )
        send_email(self.request.user, amount, 'deposit message', 'deposit_email.html')
        return super().form_valid(form)
    
class BorrowListView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'profile.html'
    context_object_name = 'records'

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrow_date')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = UserAccount.objects.get(user=self.request.user)
        context['user_balance'] = user_account.balance
        return context
    
    def post(self, request):
        user_account = request.user.account

        user_id = request.POST.get('user-id')
        borrow_id = request.POST.get('borrow-id')
        borrow_price = request.POST.get('borrow-price')

        borrow = get_object_or_404(Borrow, id=borrow_id)
            
        if borrow.user_id != int(user_id):
            return HttpResponseRedirect(reverse('profile'))
            
        borrow.is_returned = True
        user_account.balance += Decimal(borrow_price)
        user_account.save()
        borrow.save()

        return HttpResponseRedirect(reverse('profile'))  
    
   
