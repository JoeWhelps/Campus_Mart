from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listings_home'),  # Browse all listings
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='detail'),
]
