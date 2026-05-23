from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Your full name",
            "autocomplete": "name",
            "aria-label": "Full name",
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "your@email.com",
            "autocomplete": "email",
            "inputmode": "email",
            "aria-label": "Email address",
        }),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "placeholder": "How can we help?",
            "aria-label": "Subject",
        }),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5,
            "placeholder": "Tell us about your project…",
            "aria-label": "Message",
        }),
    )
    # Honeypot — if filled, reject silently
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Spam detected.")
        return cleaned
