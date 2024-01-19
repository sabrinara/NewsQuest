from django.urls import path
from . import views

urlpatterns = [
    path('details_new/<int:new_id>/', views.details_new, name='details_new'),
]