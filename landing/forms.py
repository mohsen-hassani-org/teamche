from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        fields = ("name", "email", "subject", "phone", "message")
        model = Review
        