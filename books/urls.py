from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.book_by_category, name='book_by_category'),
    path('details/<int:id>/', views.BookDetailView.as_view(), name='details'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow'),
]