from django.urls import path
from . import views
from .views import listing_detail, my_listings

app_name = "listings"

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listings_home'),  # Browse all listings
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    path('listings/<int:listing_id>/', listing_detail, name='listing_detail'),
    path('<int:listing_id>/', listing_detail, name='listing_detail'),
    path('my-listings/', my_listings, name='my_listings'),
    path('purchase/', views.purchase_listings, name='purchase_listings'),
]
