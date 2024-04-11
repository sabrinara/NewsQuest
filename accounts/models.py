from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
# Create your models here.

class UserNewspaperAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True) 
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_publish_date = models.DateField(auto_now_add=True)
    is_editor = models.BooleanField(default=False)
    userImage = models.ImageField(upload_to='accounts/media/uploads', null=True, blank=True)

    
    def __str__(self):
        return str(self.account_no)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length= 100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.email)