from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
# Create your views here.
from .models import Clients
from .tables import PersonTable

class PersonListView(SingleTableView):
    model = Clients
    table_class = PersonTable
    template_name = "clients.html"

def StartPage(request):
    return render(request, 'home.html', {})

def clients(request):
    table = PersonTable(Clients.objects.all())
    RequestConfig(request, paginate={"per_page": 2}).configure(table)


    clients = Clients.objects.all()

    return render(request, 'clients.html', {'clients': clients, 'table': table})


