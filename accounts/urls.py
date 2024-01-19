from django.urls import path
from . import views 

urlpatterns = [
   
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('changePassword2/', views.change_password2, name='changePassword2'),

]