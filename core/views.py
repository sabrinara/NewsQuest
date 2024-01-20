from django.shortcuts import render
from django.views.generic import TemplateView
from news.models import New, Rating
from django.db.models import Avg
from news.constants import CATEGORY_CHOICES


def home(request, new_category=None):
    news = New.objects.all()

    for new in news:
        # Calculate average rating for each article
        ratings = Rating.objects.filter(new=new)
        new.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    # Calculate overall average rating for all articles
    all_ratings = Rating.objects.all()
    average_rating = all_ratings.aggregate(Avg('rating'))['rating__avg']

    # Order the news by average rating in descending order
    news = sorted(news, key=lambda x: x.average_rating if x.average_rating is not None else 0, reverse=True)
    
    categories = [category[0] for category in CATEGORY_CHOICES]

    if new_category:
        news = news.filter(categories=new_category)

    return render(request, 'index.html', {'newses': news, 'categories': categories, 'average_rating': average_rating})


# generate new function to filter by categories 
def categories_filter(request, new_category):
    news = New.objects.filter(categories=new_category)
    categories = [category[0] for category in CATEGORY_CHOICES]
    return render(request, 'all_categories.html', {'newses': news, 'selected_category': new_category, 'categories': categories})

def all_categories(request, new_category):
    news = New.objects.filter(categories=new_category).order_by('-rating')
    categories = [category[0] for category in CATEGORY_CHOICES]

    for new in news:
        # Calculate average rating for each article
        ratings = Rating.objects.filter(new=new)
        new.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    # Calculate overall average rating for all articles in the category
    all_ratings = Rating.objects.filter(new__categories=new_category)
    average_rating = all_ratings.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'all_categories.html', {'newses': news, 'categories': categories, 'average_rating': average_rating, 'current_category': new_category})
