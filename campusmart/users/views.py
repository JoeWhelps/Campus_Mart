from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Django's built-in login view
    else:
        form = RegisterForm()
    return render(request, 'market/register.html', {'form': form})

