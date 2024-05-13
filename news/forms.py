from django import forms
from .models import ContactUs, News, Comment


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"


class NewsCreatedForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
            'title',
            'body',
            'image',
            'category',
            'status',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

