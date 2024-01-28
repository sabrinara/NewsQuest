from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Avg
from .models import New, Rating
from .forms import RatingForm

def send_rating_thank_you_email(user, article, rating):
    subject = 'Thank You for Your Rating!'
    template = 'news/rating_email.html'
    context = {'user': user, 'article': article, 'rating': rating}
    message = render_to_string(template, context)
    
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

def details_new(request, new_id):from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Avg
from .models import New, Rating
from .forms import RatingForm

def send_rating_thank_you_email(user, article, rating):
    subject = 'Thank You for Your Rating!'
    template = 'news/rating_email.html'
    context = {'user': user, 'article': article, 'rating': rating}
    message = render_to_string(template, context)
    
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

def details_new(request, new_id):
    article = get_object_or_404(New, pk=new_id)
    ratings = Rating.objects.filter(new=article)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    # Fetch two related articles in the same category, excluding the current article
    related_articles = New.objects.filter(categories=article.categories).exclude(id=article.id).order_by('-rating')[:2]

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            user_rating = form.cleaned_data['rating']
            rating_instance = Rating.objects.create(user=request.user, new=article, rating=user_rating)

            # Send thank-you email to the user
            send_rating_thank_you_email(request.user, article, user_rating)

            messages.success(request, 'Thank you for your rating!')

            return HttpResponseRedirect(reverse('details_new', args=(new_id,)))
    else:
        form = RatingForm()

    context = {
        'article': article,
        'ratings': ratings,
        'average_rating': average_rating,
        'form': form,
        'related_articles': related_articles,
    }

    return render(request, 'news/details_new.html', context)

    # news = New.objects.all()
    # article = get_object_or_404(New, pk=new_id)
    # ratings = Rating.objects.filter(new=article)
    # average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    # if request.method == 'POST':
    #     form = RatingForm(request.POST)
    #     if form.is_valid():
    #         user_rating = form.cleaned_data['rating']
    #         rating_instance = Rating.objects.create(user=request.user, new=article, rating=user_rating)

    #         # Send thank-you email to the user
    #         send_rating_thank_you_email(request.user, article, user_rating)

    #         messages.success(request, 'Thank you for your rating!')

    #         return HttpResponseRedirect(reverse('details_new', args=(new_id,)))
    # else:
    #     form = RatingForm()

    # context = {
    #     'article': article,
    #     'ratings': ratings,
    #     'average_rating': average_rating,
    #     'form': form,
    #     'newses': news,
    # }

    # return render(request, 'news/details_new.html', context)
