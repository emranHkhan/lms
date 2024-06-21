from django.db import models
from categories.models import Category

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.name
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')

    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField()
    review_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Reviewed By {self.reviewer_name}"