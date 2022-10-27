# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms

class LoginForm(forms.Form):
    fullName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g: Profession",
                "class": "form-control"
            }
        ))