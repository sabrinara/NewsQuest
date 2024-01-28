from django.contrib import admin
from .models import UserNewspaperAccount, UserAddress
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

# Register your models here.

# for editor approval
def send_email(user,subject, template):
    message = render_to_string(template, {
        'user' : user,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_editor']

    def save_model(self, request, obj, form, change):
        obj.save()
        send_email(obj.user,"Editor Approval", "accounts/editor_email.html")
        super().save_model(request, obj, form, change)

admin.site.register(UserNewspaperAccount, UserAccountAdmin)
admin.site.register(UserAddress)
