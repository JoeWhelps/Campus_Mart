from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User
from django.forms.models import model_to_dict

def register(request):
    if request.POST:
        # Create a model instance and populate it with data from the request
        name = request.POST.get("name", "")
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        user = User(name=name, username=username, email=email, password=password)

        errors = []
        if not name or not username or not email or not password: #make sure all fields are inputted
            errors.append(("validation", "All fields are required."))

        if User.objects.filter(username=username).exists(): #make sure that username is not already in use
            errors.append(("username", "Username already in use"))
        if User.objects.filter(email=email).exists(): #make sure that email is not already in use
            errors.append(("email", "Email already in use"))
        
        try:
            user.full_clean()
            user.password = make_password(password)  # encrypts
            # if we reach here, the validation succeeded
            user.save()  # saves on the db
            # redirect to the login page
            return HttpResponseRedirect(reverse('polls:login'))
        except ValidationError as e:
            errors.extend([(field, err[0]) for field, err in e.message_dict.items()])
            return render(request, "polls/register.html", {
                "errors": errors,
                "values": model_to_dict(user)
            })
        return HttpResponseRedirect(reverse('polls:login'))

    return render(request, "polls/register.html")