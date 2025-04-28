from django.shortcuts import render, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

class ListingCreateView(CreateView):
    model = Listing
    fields = ['title', 'description', 'price', 'condition', 'photo']
    template_name = 'market/createListings.html'
    success_url = reverse_lazy('marketplace:home')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    

class ListingUpdateView(UpdateView):
    model = Listing
    fields = ['title', 'description', 'price', 'condition', 'status']
    template_name = 'market/update_listing.html'
    success_url = reverse_lazy('marketplace:home')


class ListingDeleteView(DeleteView):
    model = Listing
    template_name = 'market/delete_listing.html'
    success_url = reverse_lazy('marketplace:home')



class ListingListView(ListView):
    model = Listing
    template_name = 'market/listings.html'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Listing.objects.filter(title__icontains=query)
        return Listing.objects.all()


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'market/listing_detail.html'

# views.py

def listing_detail(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        data = {
            'title': listing.title,
            'description': listing.description,
            'photo_url': listing.photo.url,
            'price': listing.price,
            'contact': listing.seller.username,  # Assuming seller is the contact
        }
        return JsonResponse(data)
    except Listing.DoesNotExist:
        return JsonResponse({'error': 'Listing not found'}, status=404)

