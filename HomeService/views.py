from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
# Create your views here.
from .models import Clients
from .tables import PersonTable
from .forms import ClientForm

def StartPage(request):
    return render(request, 'home.html', {})


def clients(request):
    table = PersonTable(Clients.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(table)
    return render(request, 'clients.html', {'table': table})


def client_detail(request, pk):
    client = get_object_or_404(Clients, pk=pk)
    form = ClientForm(instance=client)
    return render(request, 'client_detail.html', {'form': form})


