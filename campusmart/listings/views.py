from django.shortcuts import render, redirect
from .models import Listing, ListingPurchase
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import requests
from django.contrib import messages
from django.conf import settings
from django.utils import timezone


# Create your views here.

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView


class ListingCreateView(CreateView):
    model = Listing
    fields = ['title', 'description', 'price', 'condition', 'photo']
    template_name = 'market/createListings.html'
    success_url = reverse_lazy('marketplace:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate remaining listings
        # Count every purchase in the last 24 hours
        total_purchased_today = sum(purchase.amount for purchase in ListingPurchase.objects.filter(
            user=self.request.user,
            purchase_date__gte=timezone.now() - timezone.timedelta(days=1),
            purchase_date__lte=timezone.now()
        ))
        current_listings = Listing.objects.filter(seller=self.request.user).count()
        today_listings = Listing.objects.filter(
            seller=self.request.user,
            created_at__date=timezone.now().date()
        ).count()
        
        # Calculate remaining free listings for today
        free_listings_remaining = max(0, 4 - today_listings)
        

        # Calculate remaining purchased listings
        # Only count listings beyond the free limit (4 per day) against purchased listings
        if free_listings_remaining == 0:
            purchased_listings_remaining = max(0, total_purchased_today - today_listings)
        else:
            purchased_listings_remaining = total_purchased_today
        
        # Total remaining listings is free + purchased
        context['remaining_listings'] = free_listings_remaining + purchased_listings_remaining
        context['free_listings_remaining'] = free_listings_remaining
        context['purchased_listings_remaining'] = purchased_listings_remaining
        return context

    def form_valid(self, form):
        # Get current listing counts
        today_listings = Listing.objects.filter(
            seller=self.request.user,
            created_at__date=timezone.now().date()
        ).count()
        
        total_purchased = sum(purchase.amount for purchase in ListingPurchase.objects.filter(user=self.request.user))
        current_listings = Listing.objects.filter(seller=self.request.user).count()
        
        # Calculate listings beyond free limit
        listings_beyond_free = max(0, current_listings - 4)
        
        # Check if user has any remaining listings
        if today_listings >= 4 and listings_beyond_free >= total_purchased:
            messages.error(self.request, 'You have reached your daily limit of 4 free listings and have no remaining purchased listings. Please purchase additional listings with Krato$Coin to create more.')
            return redirect('listings:purchase_listings')
        
        # If we get here, user has either free listings remaining or purchased listings
        form.instance.seller = self.request.user
        
        # Create the listing
        response = super().form_valid(form)
        
        # Update the listing counts after creation
        new_today_listings = Listing.objects.filter(
            seller=self.request.user,
            created_at__date=timezone.now().date()
        ).count()
        
        # If we've exceeded free listings, we should have purchased listings available
        if new_today_listings > 4 and listings_beyond_free >= total_purchased:
            # This should never happen due to our earlier check, but just in case
            messages.error(self.request, 'Error: Unable to create listing. Please try again.')
            return redirect('listings:purchase_listings')
            
        return response
    

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

@login_required
def my_listings(request):
    # Get all listings where the seller is the currently logged-in user
    listings = Listing.objects.filter(seller=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})

@login_required
def purchase_listings(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount <= 0:
            messages.error(request, 'Please enter a valid amount of listings to purchase.')
            return redirect('listings:purchase_listings')
        
        # Get access token (you'll need to implement token storage/retrieval)
        access_token = settings.KRATO_API_TOKEN
        
        # Make API request to check balance and process payment
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # First check balance
        balance_response = requests.get(
            f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/{request.user.email}/",
            headers=headers
        )
        
        if balance_response.status_code != 200:
            messages.error(request, 'Failed to check your Krato$Coin balance.')
            return redirect('listings:purchase_listings')
            
        balance = balance_response.json()['amount']
        
        if balance < amount:
            messages.error(request, f'Insufficient Krato$Coin balance. You have {balance} coins.')
            return redirect('listings:purchase_listings')
            
        # Process payment
        payment_response = requests.post(
            f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/{request.user.email}/pay",
            headers=headers,
            json={"amount": amount}
        )
        
        if payment_response.status_code == 200:
            # Create purchase record
            ListingPurchase.objects.create(user=request.user, amount=amount)
            messages.success(request, f'Successfully purchased {amount} additional listings!')
            return redirect('marketplace:create')
        else:
            messages.error(request, 'Failed to process payment. Please try again.')
            return redirect('listings:purchase_listings')
            
    # Get current balance for display
    access_token = settings.KRATO_API_TOKEN
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    balance_response = requests.get(
        f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/{request.user.email}/",
        headers=headers
    )
    
    balance = 0
    if balance_response.status_code == 200:
        balance = balance_response.json()['amount']
    
    # Get current purchase history
    purchases = ListingPurchase.objects.filter(user=request.user).order_by('-purchase_date')
    total_purchased = sum(purchase.amount for purchase in purchases)
    
    return render(request, 'listings/purchase_listings.html', {
        'balance': balance,
        'total_purchased': total_purchased,
        'purchases': purchases
    })
