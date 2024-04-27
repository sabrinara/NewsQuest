
from django.shortcuts import render,redirect, get_object_or_404
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Avg
from .models import New, Rating
from .forms import RatingForm, newsForm

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



# editor delete and edit 
@login_required
def edit_news(request, id):
    post = New.objects.get(id=id)
    
    if request.user.account.is_editor:
        if request.method == 'POST':
            form = newsForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'News updated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid form submission.')
        else:
            form = newsForm(instance=post)
            
        return render(request, 'news/add_news.html', {'form': form})
    else:
        messages.warning(request, 'No permission to edit.')
        return redirect('home')

@login_required
def delete_news(request, id):
    post = New.objects.get(id=id)
    
    if request.user.account.is_editor:
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'News deleted successfully.')
            return redirect('home')
        else:
            return render(request, 'news/delete_news.html', {'post': post})
    else:
        messages.warning(request, 'No permission to delete.')
        return redirect('home')
    
@login_required
def add_news(request):
    if request.user.account.is_editor:
        if request.method == 'POST':
            form = newsForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                messages.success(request, ' added successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid form submission.')
                print(form.errors)
        else:
            form = newsForm()
        
        return render(request, 'news/add_news.html', {'form': form})
    else:
        messages.warning(request, 'No permission to add.')
        return redirect('home')
    

@login_required
def all_news(request):
    newses = New.objects.all()
    return render(request, 'news/all_news.html', {'newses': newses})



@login_required
@login_required
def top_rated_news(request):
    top_rated_newses = New.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:6]
    return render(request, 'news/newshome.html', {'newses': top_rated_newses})


def about(request):
    return render(request, 'news/about.html')
