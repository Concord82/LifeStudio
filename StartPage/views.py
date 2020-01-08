from django.shortcuts import render

# Create your views here.


def StartPage(request):
    return render(request, 'startpage.html', {})