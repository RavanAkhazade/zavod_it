from django import forms
from .models import News


class CreateNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "text", "tags"]
