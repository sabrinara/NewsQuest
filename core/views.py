from django.shortcuts import render
from django.views.generic import TemplateView
from news.models import New
from news.constants import CATEGORY_CHOICES
# Create your views here.

def home(request, new_category=None):
    news = New.objects.all()
    categories = [category[0] for category in CATEGORY_CHOICES]
    for new in news: 
        print(new)
    newCategory = new_category
    if new_category:
        news = news.filter(categories=newCategory)
     
    return render(request, 'index.html', {'newses': news, 'categories': categories})