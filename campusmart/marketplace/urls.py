from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "marketplace"

urlpatterns = [
    path('', login_required(views.home_view), name='home'),
    path('welcome/', views.welcome, name= 'welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/',views.home_view, name='home'),
    path('create/', views.createListings, name='create'),
]

