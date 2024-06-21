from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username + "'s account"

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrow_date = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    balance_after_transaction = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user.username} - {self.book.name}"
