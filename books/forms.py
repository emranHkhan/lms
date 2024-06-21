from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['reviewer_name', 'reviewer_email', 'review_text']