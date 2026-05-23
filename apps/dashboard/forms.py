from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.pages.models import Service, Project, Testimonial


class DashboardLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "title", "slug", "description", "long_description",
            "what_we_offer", "our_process", "meta_description",
            "icon_name", "order", "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "long_description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "what_we_offer": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "One item per line"}),
            "our_process": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "One step per line"}),
            "meta_description": forms.TextInput(attrs={"class": "form-control"}),
            "icon_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. code, smartphone, search"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "slug", "url", "category", "filter_group",
            "image", "full_description", "tech_stack", "client_name", "year", "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "filter_group": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "full_description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "tech_stack": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Django, React, PostgreSQL"}),
            "client_name": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2024"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "role", "quote", "avatar", "order", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "quote": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
