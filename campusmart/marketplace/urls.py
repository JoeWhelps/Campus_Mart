from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path('', views.home_view, name='home'),  # default home route
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('listings/', views.ListingListView.as_view(), name='listings_home'),
    path('listings/create/', views.ListingCreateView.as_view(), name='create'),
    path('listings/<int:pk>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('listings/<int:pk>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('api/listings/<int:listing_id>/', views.get_listing_details, name='get_listing_details'),
]

'''
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "marketplace"

urlpatterns = [
    path('', login_required(views.home_view), name='home'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('welcome/', views.welcome, name= 'welcome'),
    path('register/', views.register, name='register'),
    #path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/',views.home_view, name='home'),
    path('create/', views.createListings, name='create'),
]
'''

