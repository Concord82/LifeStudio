from django.urls import path

from . import views
urlpatterns = [
    path('', views.StartPage),
    path('clients/', views.clients, name='clients'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),

]