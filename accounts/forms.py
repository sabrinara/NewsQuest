from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserNewspaperAccount, UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    profile_pic = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date', 'gender', 'profile_pic', 'postal_code', 'city', 'country', 'street_address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account = UserNewspaperAccount.objects.create(
                user=user,
                gender=self.cleaned_data['gender'],
                birth_date=self.cleaned_data['birth_date'],
                account_no=100000 + user.id
            )

            user_address = UserAddress.objects.create(
                user=user,
                postal_code=self.cleaned_data['postal_code'],
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                street_address=self.cleaned_data['street_address']
            )

            if 'profile_pic' in self.cleaned_data:
                user_account.profile_pic = self.cleaned_data['profile_pic']
                user_account.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserNewspaperAccount.DoesNotExist:
                user_account = None
                user_address = None

        if user_account:
            self.fields['gender'].initial = user_account.gender
            self.fields['birth_date'].initial = user_account.birth_date
            self.fields['street_address'].initial = user_address.street_address
            self.fields['city'].initial = user_address.city
            self.fields['postal_code'].initial = user_address.postal_code
            self.fields['country'].initial = user_address.country
            # self.fields['profile_pic'].initial = user_account.profile_pic
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
