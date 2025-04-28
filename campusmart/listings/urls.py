from django.urls import path
from . import views
from .views import listing_detail

app_name = "listings"

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listings_home'),  # Browse all listings
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    #path('<int:pk>/', views.ListingDetailView.as_view(), name='detail'),
    path('listings/<int:listing_id>/', listing_detail, name='listing_detail'),
    path('<int:listing_id>/', listing_detail, name='listing_detail'),
]
