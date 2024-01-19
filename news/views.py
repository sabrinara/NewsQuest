from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms, models
from accounts.models import UserNewspaperAccount
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import New, Rating
from .forms import RatingForm
from django.db.models import Avg
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# def send_borrow_email(user, amount, subject, template, current_balance):
#     message = render_to_string(template, {'user': user,'amount': amount,'current_balance': current_balance,})
#     send_email = EmailMultiAlternatives(subject, '', to=[user.email])
#     send_email.attach_alternative(message, 'text/html')
#     send_email.send()


# def details_new(request, new_id):
#     new = get_object_or_404(models.new, id=new_id)
#     user = request.user

#     if request.method == 'POST':


#     return render(request, 'news/details_new.html', {'new': new})

def details_new(request, new_id):
    news = New.objects.all()
    article = get_object_or_404(New, pk=new_id)
    ratings = Rating.objects.filter(new=article)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            user_rating = form.cleaned_data['rating']
            Rating.objects.create(user=request.user, new=article, rating=user_rating)
            return HttpResponseRedirect(reverse('details_new', args=(new_id,)))
    else:
        form = RatingForm()

    context = {
        'article': article,
        'ratings': ratings,
        'average_rating': average_rating,
        'form': form,
        'newses': news,
        
    }

    return render(request, 'news/details_new.html', context)

