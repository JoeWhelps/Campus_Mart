from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'marketplace/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After signup, go to login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

