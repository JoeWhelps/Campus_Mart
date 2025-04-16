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

def welcome(request):
    return render(request, 'market/welcome.html')

def home_view(request):
    user_obj = None
    if "user" in request.session:
        user_obj = User.objects.filter(username=request.session["user"]).first()
    return render(request, 'market/home.html', {'user_obj': user_obj})


def register(request):
    print("ahhhhhhh")
    if request.POST:
        print("okkka")
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

        # Encrypt password BEFORE saving or validating
        hashed_password = make_password(password)
        user = User(name=name, username=username, email=email, password=hashed_password)

        try:
            user.full_clean()
            user.save()
            return HttpResponseRedirect(reverse('marketplace:login'))
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "market/register.html", {
                "errors": errors,
                "values": {"name": name, "username": username, "email": email}
            })

    return render(request, "market/register.html")


def login(request):
    errors = None
    if request.POST:
        # Create a model instance and populate it with data from the request
        uname = request.POST["username"]
        pwd = request.POST["password"]
        user = User.objects.filter(username=uname)

        if len(user) > 0 and check_password(pwd, user[0].password):
            # create a new session
            request.session["user"] = uname
            return HttpResponseRedirect(reverse('marketplace:home'))
        else:
            errors = [('authentication', "Login error")]

    return render(request, 'market/login.html', {'errors': errors})


def createListings(request):
    if request.POST:
        # Create a model instance and populate it with data from the request
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        price = request.POST.get("price", "")
        condition = request.POST.get("condition", "")
        status = request.POST.get("status", "")
        photo = request.POST.get("photo", "")

        listing = Listing(title=title, description=description, price=price, condition=condition, status=status, photo=photo)

        errors = []
        if not title or not description or not price or not condition or not status or not photo: #make sure all fields are inputted
            errors.append(("validation", "All fields are required."))

        
        try:
            listing.full_clean()
            listing.save()  # saves on the db
            # redirect to the login page
            return HttpResponseRedirect(reverse('marketplace:login'))
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "market/createListing.html", {
                "errors": errors,
                "values": model_to_dict(listing)
            })
        return HttpResponseRedirect(reverse('login'))

    return render(request, "market/createListing.html")


def logout(request):
    # remove the logged-in user information
    del request.session["user"]
    return HttpResponseRedirect(reverse("marketplace:login"))

'''
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After signup, go to login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
'''