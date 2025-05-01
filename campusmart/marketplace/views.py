from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib import messages
from django.utils import timezone
from listings.models import Listing, ListingPurchase

@login_required
def home_view(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(title__icontains=query) if query else Listing.objects.all()
    return render(request, 'market/home.html', {'listings': listings, 'query': query})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")

        errors = []
        if not all([username, password, email, name]):
            errors.append(("validation", "All fields are required."))
        if User.objects.filter(username=username).exists():
            errors.append(("username", "Username already in use"))
        if User.objects.filter(email=email).exists():
            errors.append(("email", "Email already in use"))

        if errors:
            return render(request, "market/register.html", {
                "errors": errors,
                "values": {"name": name, "username": username, "email": email}
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )
            login(request, user)
            return redirect('marketplace:home')
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "market/register.html", {
                "errors": errors,
                "values": {"name": name, "username": username, "email": email}
            })

    return render(request, "market/register.html")

class ListingCreateView(CreateView):
    model = Listing
    fields = ['title', 'description', 'price', 'condition', 'photo']
    template_name = 'market/createListings.html'
    success_url = reverse_lazy('marketplace:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_purchased = sum(purchase.amount for purchase in ListingPurchase.objects.filter(user=self.request.user))
        current_listings = Listing.objects.filter(seller=self.request.user).count()
        today_listings = Listing.objects.filter(
            seller=self.request.user,
            created_at__date=timezone.now().date()
        ).count()
        
        free_listings_remaining = max(0, 4 - today_listings)
        context['remaining_listings'] = free_listings_remaining + total_purchased - current_listings
        context['free_listings_remaining'] = free_listings_remaining
        return context

    def form_valid(self, form):
        today_listings = Listing.objects.filter(
            seller=self.request.user,
            created_at__date=timezone.now().date()
        ).count()
        
        total_purchased = sum(purchase.amount for purchase in ListingPurchase.objects.filter(user=self.request.user))
        current_listings = Listing.objects.filter(seller=self.request.user).count()
        
        if today_listings >= 4 and current_listings >= total_purchased:
            messages.error(self.request, "You have reached your daily listing limit and have no purchased listings remaining.")
            return self.form_invalid(form)
        
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
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'market/listing_detail.html'

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'market/listing_detail.html', {'listing': listing})

@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})

@login_required
def logout(request):
    django_logout(request)
    return redirect('marketplace:home')

@login_required
@require_GET
def get_listing_details(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    data = {
        'title': listing.title,
        'description': listing.description,
        'price': listing.price,
        'condition': listing.condition,
        'status': listing.status,
        'created_at': listing.created_at.strftime('%B %d, %Y'),
        'updated_at': listing.updated_at.strftime('%B %d, %Y') if hasattr(listing, 'updated_at') else None,
        'seller_username': listing.seller.username,
        'seller_email': listing.seller.email,
        'seller_id': listing.seller.id,
        'photo_url': listing.photo.url if listing.photo else '',
    }
    return JsonResponse(data) 