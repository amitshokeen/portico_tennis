from django import forms
from .models import CustomUser

#class CustomUserCreationForm(UserCreationForm):
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']
