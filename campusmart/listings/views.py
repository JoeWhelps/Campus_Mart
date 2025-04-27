from django.shortcuts import render, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required

# Create your views here.

def create_listing(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        photo = request.FILES.get('photo')

        if not (title and description and price and condition and photo):
            return render(request, 'listings/create_listing.html', {'error': 'All fields are required.'})

        # Create and save the new Listing
        listing = Listing.objects.create(
            title=title,
            description=description,
            price=price,
            condition=condition,
            photo=photo,
            seller=request.user
        )
        return redirect('marketplace:listings')  

    return render(request, 'listings/create_listing.html')

