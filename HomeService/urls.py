from django.urls import path

from . import views
urlpatterns = [
    path('', views.StartPage),
    path('clients/', views.clients, name='clients'),

path('clients2/', views.PersonListView.as_view()),


]