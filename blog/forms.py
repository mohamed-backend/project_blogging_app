# blogging_platform/blog/forms.py

from django import forms
from .models import Post


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']