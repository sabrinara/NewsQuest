from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_news, name='add_news'),
    path('edit/<int:id>/',views.edit_news, name='edit_news'),
    path('delete/<int:id>/',views.delete_news, name='delete_news'),
    path('details_new/<int:new_id>/', views.details_new, name='details_new'),
]