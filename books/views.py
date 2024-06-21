from django.shortcuts import redirect, render
from categories.models import Category
from .models import Book
from .import forms
from django.views.generic import DetailView
from users.models import Borrow
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_email(user, book_name, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'book_name' : book_name,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


def book_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    books = Book.objects.filter(category=category)
    
    return render(request, 'home.html', {'selected_category': category, 'books': books, 'categories': categories})

class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_detail.html'

    def post(self, request):
        self.object = self.get_object()
        review_form = forms.ReviewForm(data=request.POST)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = self.object
            new_review.user = request.user
            new_review.save()
            return redirect('details', id=self.object.id)

        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = forms.ReviewForm()

        
        user_has_borrowed = False
        if self.request.user.is_authenticated:
            user_has_borrowed = Borrow.objects.filter(user=self.request.user, book=book).exists()
        
       
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['user_has_borrowed'] = user_has_borrowed
        return context
    

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)

    borrowed_book = Borrow.objects.filter(user=request.user, book=book).first()

    if borrowed_book and not borrowed_book.is_returned:
        messages.error(request, f'You have already borrowed the book')
        return redirect(request.META.get('HTTP_REFERER', '/'))  

    else:
        if book.quantity > 0:  
            if request.method == 'POST':
                user_account = request.user.account
                book_borrow_price = book.borrow_price

                if user_account.balance >= book_borrow_price: 
                    borrow = Borrow(user=request.user, book=book)
                    borrow.balance_after_transaction = user_account.balance - book_borrow_price
                    borrow.save()

                    book.quantity -= 1
                    book.save()
                    
                    user_account.balance -= book_borrow_price
                    user_account.save()
                    send_email(request.user, book.name, "borrow message", "borrow_book_email.html")
                    messages.success(request, f'Successful! an email has been sent to your account.')
                else:
                    messages.error(request, 'Insufficient balance to borrow the book.')
                    return redirect('deposit')

                return redirect('home')
            
            return render(request, 'home', {'book': book})
        else:
            messages.error(request, f'Sorry, {book.name} is no longer available.')
            return redirect('home')
    


