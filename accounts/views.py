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

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            messages.success(request, 'Signup successful. Please login.')
            return redirect('login')
    else:
        form = forms.UserRegistrationForm()

    return render(request, 'accounts/registration.html', {'form': form, 'title': 'Sign Up'})

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