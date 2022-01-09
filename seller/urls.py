from django.urls import path

from . import views

urlpatterns = [
    path('addlisting', views.addlisting, name='addlisting'),
    path('listing_sub', views.listing_sub, name='listing_sub')
]