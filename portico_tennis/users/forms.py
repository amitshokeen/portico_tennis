from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import PasswordResetForm

# Invitation codes are hard-coded here. Not the best practice. 
# To be improved: 1. store codes in a db and validate against them dynamically.
# 2. Use of regex patterns to match invitation code formats
# 3. Use e-mail to send one time codes and verify them... this can be interesting...
INVITATION_CODES = ["TENNIS2025", "tennis2025", "PLAY2025", "play2025", "testnow"]

class CustomUserCreationForm(UserCreationForm):
    invitation_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter invitation code', 
            'id': 'id_invitation_code',
            'autofocus': True
        }),
        label="Invitation Code"
    )
    def clean_invitation_code(self):
        code = self.cleaned_data.get('invitation_code')
        if code not in INVITATION_CODES:
            raise forms.ValidationError("Invalid invitation code.")
        return code
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        label="Email Address"
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        }),
        label="Phone Number"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'invitation_code']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Bootstrap styling
            'placeholder': 'Enter your username'
        }),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-input',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        }),
        label="Password"
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email to reset your password',
            'id': 'id_email'
        }),
        label="Email Address"
    )