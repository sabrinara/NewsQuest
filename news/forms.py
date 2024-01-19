from django import forms
from . import models

class newsForm(forms.ModelForm):
    class Meta:
        model = models.New
        fields = ['categories', 'title','image', 'description',  'publishing_time']
