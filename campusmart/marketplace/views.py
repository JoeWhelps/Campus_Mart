from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict
from .models import User, Listing 
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as django_logout
from .models import User, Listing
from django.shortcuts import render
from listings.models import Listing

@login_required
def home_view(request):
    listings = Listing.objects.all()
    return render(request, 'market/home.html', {'listings': listings})



def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        errors = []
        if not name or not username or not email or not password:
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

        # Hash password & save user
        hashed_password = make_password(password)
        user = User(name=name, username=username, email=email, password=hashed_password)

        try:
            user.full_clean()
            user.save()
            # Auto-login the user
            auth_user = authenticate(request, username=username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('login')
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "market/register.html", {
                "errors": errors,
                "values": {"name": name, "username": username, "email": email}
            })

    return render(request, "market/register.html")


@login_required
def createListings(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        price = request.POST.get("price", "")
        condition = request.POST.get("condition", "")
        status = request.POST.get("status", "")
        photo = request.POST.get("photo", "")

        listing = Listing(title=title, description=description, price=price, condition=condition, status=status, photo=photo)

        errors = []
        if not all([title, description, price, condition, status, photo]):
            errors.append(("validation", "All fields are required."))

        try:
            listing.full_clean()
            listing.save()
            return redirect('marketplace:home')
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "market/createListing.html", {
                "errors": errors,
                "values": model_to_dict(listing)
            })

    return render(request, "market/createListings.html")


def logout(request):
    django_logout(request)
    return redirect('login')
