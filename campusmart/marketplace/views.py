from django.shortcuts import render


def home(request):
    return render(request, 'marketplace/templates/marketplace/home.html')
