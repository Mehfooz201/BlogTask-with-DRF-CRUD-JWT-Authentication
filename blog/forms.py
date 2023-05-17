from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from .models import BlogPost

class SignupForm(UserCreationForm):
    password1= forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name':'First Name', 'last_name': 'Last Name', 'email':'Email'}
        
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.TextInput(attrs={'class':'form-control'}) }

class loginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))



class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'tags']
        labels = {'title':'Title', 'content': 'Content', 'tags':'Tags'}
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.host = self.request.user
        if commit:
            instance.save()
        return instance