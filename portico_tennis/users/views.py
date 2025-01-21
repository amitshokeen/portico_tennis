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
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@ratelimit(key='ip', rate='5/m', block=True)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user as inactive
            user = form.save(commit=False) # Save but don't commit to DB yet
            user.is_active = False # Admin will activate manually
            user.save()
    
            # Send email to the admin
            try:
                send_mail(
                    subject='New User Registration Request',
                    message=f'A new user wants to play tennis at Portico:\n\nUsername: {user.username}\nEmail: {user.email}\nPhone Number: {user.phone_number}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],  # Add the admin email in settings
                )
            except Exception as e:
                messages.error(request, "There was an issue sending an email. Please try again later.")
                return render(request, 'users/register.html', {'form': form})
            
            # # Notify the user to wait for approval
            # return render(request, 'users/registration_pending.html', {
            #     'message': 'Your registration request has been submitted. Please wait up to 24 hours for admin approval.'
            # })

            # Redirect to avoid accidental resubmission on refresh
            return redirect('registration_pending')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
@ratelimit(key='ip', rate='3/m', block=True)
def home(request):
    return render(request, 'home.html')

@ratelimit(key='post:username', rate='3/m', block=True)
@ratelimit(key='ip', rate='3/m', block=True)
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

@method_decorator(ratelimit(key='ip', rate='3/m', block=True), name='dispatch')
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    success_message = "Password reset instructions have been sent to your email."