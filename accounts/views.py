from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm ,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link.")
        return redirect('signup')

def signup(request):
    if not request.user.is_authenticated:
        form = forms.UserRegistrationForm()
        if request.method == 'POST':
            form = forms.UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False  # The user is inactive until activation
                user.save()

                # Generate activation link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                current_site = get_current_site(request)
                confirm_link = f'https://{current_site.domain}/accounts/activate/{uid}/{token}'
                # confirm_link = f'https://newsquest.onrender.com/accounts/activate/{uid}/{token}'
                # confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}'

                # Send activation email
                email_subject = "Confirm your email"
                email_body = render_to_string(
                    'accounts/confirmationMail.html',
                    {'user': user, 'confirm_link': confirm_link}
                )
                email = EmailMultiAlternatives(
                     email_subject,
                     '',to = [user.email]
                )
                email.attach_alternative(email_body, 'text/html')
                email.send()

                messages.success(
                    request, 'Check your email and click on the link to activate your account.')
                return redirect('login')

        else:
            form = forms.UserRegistrationForm()

        return render(request, 'accounts/registration.html', {'form': form, 'title': 'Sign Up'})
    else:
        return redirect('home')
    
    
# def signup(request):
#     if request.method == 'POST':
#         form = forms.UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print(form.cleaned_data)
#             messages.success(request, 'Signup successful. Please login.')
#             return redirect('login')
#     else:
#         form = forms.UserRegistrationForm()

#     return render(request, 'accounts/registration.html', {'form': form, 'title': 'Sign Up'})

def user_login(request):
    if request.method == 'POST':
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           user = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=user, password=password)
           if user is not None:
               login(request, user)
               messages.success(request, 'You have successfully logged in.')
               return redirect('profile')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form , 'title': 'Login'})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# @login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html')
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid(): 
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form , 'title': 'Change Password'})

def change_password2(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid(): 
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = SetPasswordForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form, 'title': 'Change without old Password'})


class UserProfileUpdateView(LoginRequiredMixin,View):
    template_name = './accounts/update_profile.html'

    def get(self, request):
        form = forms.UserUpdateForm(instance=request.user) 
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):  
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            print(form.errors)