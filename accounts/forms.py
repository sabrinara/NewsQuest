from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import  GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserNewspaperAccount, UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date','gender', 'postal_code', 'city','country', 'street_address']
        
        
    def save(self, commit=True):
        our_user = super().save(commit=False) 
        if commit == True:
            our_user.save() 
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            
            UserAddress.objects.create(
                user = our_user,
                postal_code = postal_code,
                country = country,
                city = city,
                street_address = street_address
            )
            UserNewspaperAccount.objects.create(
                user = our_user,
                gender = gender,
                birth_date =birth_date,
                account_no = 100000+ our_user.id
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })



class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    profile_pic = forms.ImageField()  # Make the profile_pic field not required

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_pic']  # Include 'profile_pic' in fields

    # Add this method to handle profile picture update
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserNewspaperAccount.objects.get_or_create(user=user) 
            user_address, created = UserAddress.objects.get_or_create(user=user) 

            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            if 'profile_pic' in self.cleaned_data:  # Check if profile_pic is in cleaned_data
                user_account.profile_pic = self.cleaned_data['profile_pic']  # Set profile_pic if available
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
