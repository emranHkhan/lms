from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('profile/', views.BorrowListView.as_view(), name='profile'),
]
