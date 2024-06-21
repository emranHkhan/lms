from django.shortcuts import render
from books.models import Book
from categories.models import Category

def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})