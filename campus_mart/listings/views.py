from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from .models import BlogPost


#@login_required
def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'listings/index.html', {'posts': posts})

def view_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'listings/view.html', {'post': post})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("listings:index")  # Redirect to listings home
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
