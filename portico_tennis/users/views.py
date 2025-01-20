from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user as inactive
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request, user)
            # return redirect('home')
            # Send email to the admin
            send_mail(
                subject='New User Registration Request',
                message=f'A new user wants to play tennis at Portico:\n\nUsername: {user.username}\nEmail: {user.email}\nPhone Number: {user.phone_number}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],  # Add the admin email in settings
            )
            
            # Notify the user to wait for approval
            return render(request, 'users/registration_pending.html', {
                'message': 'Your registration request has been submitted. Please wait up to 24 hours for admin approval.'
            })
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password. Please try again. Note that both fields may be case-sensitive.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to login page

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    success_message = "Password reset instructions have been sent to your email."