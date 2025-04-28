from django.shortcuts import render, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

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


'''

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

'''