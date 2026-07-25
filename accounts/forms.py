from django import forms
from django.contrib.auth.models import User
from .models import Seller, Customer


class SellerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Seller
        fields = ['shop_name', 'shop_description', 'phone', 'image', 'pan_number']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Shop Name'}),
            'shop_description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Describe your shop...', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PAN Number'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['email'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Email Address'})
            self.fields['first_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'First Name'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Last Name'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            self.user.save()
        return profile


class CustomerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['phone', 'image', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Your Address', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['email'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Email Address'})
            self.fields['first_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'First Name'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Last Name'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            self.user.save()
        return profile
