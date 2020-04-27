from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('listing', views.listing,name='listing'),
    path('search', views.search,name='search'),
    path('data', views.data,name='data'),
    
    path('detail/<int:id>', views.detail,name='detail'),
    
  
]