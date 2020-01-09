from django.shortcuts import render

# Create your views here.
from .models import Clients


def StartPage(request):
    return render(request, 'home.html', {})

def clients(request):
    clients = Clients.objects.all()

    return render(request, 'clients.html', {'clients': clients})


