from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms, models
from accounts.models import UserNewspaperAccount
from decimal import Decimal
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# def send_borrow_email(user, amount, subject, template, current_balance):
#     message = render_to_string(template, {'user': user,'amount': amount,'current_balance': current_balance,})
#     send_email = EmailMultiAlternatives(subject, '', to=[user.email])
#     send_email.attach_alternative(message, 'text/html')
#     send_email.send()


def details_new(request, new_id):
    new = get_object_or_404(models.new, id=new_id)
    user = request.user

    # if request.method == 'POST':


    return render(request, 'news/details_new.html', {'new': new})