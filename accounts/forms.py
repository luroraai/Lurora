#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 12.02.2025 19:24
#  Filename : forms.py
#  Last Modified : 12.02.2025 19:24
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, label='E-posta',
                             widget=forms.TextInput(attrs={'placeholder': 'mail@mail.com'}))
    password = forms.CharField(max_length=20, label='Parola',
                               widget=forms.PasswordInput(attrs={"placeholder": "*******"}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        values = {
            "email": email,
            "password": password
        }

        return values


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error("email", "Bu e-posta adresi ile daha önce kayıt olunmuş!")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
