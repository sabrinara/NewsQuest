from django import forms
from . import models

class newsForm(forms.ModelForm):
    class Meta:
        model = models.New
        fields = ['categories', 'title','image', 'description',  'publishing_time']


class RatingForm(forms.ModelForm):
    class Meta:
        model = models.Rating
        fields = ['rating']

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = models.Category
#         fields = ['name']
#         exclude = ['slug']