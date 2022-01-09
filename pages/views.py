from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import price_choices, bedroom_choices, state_choices, locations
from django.db.models import F

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'state_choices' : state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'locations':locations
    }
    return render(request, 'pages/index.html', context)

def about(request):
    
    realtors= Realtor.objects.order_by('-hire_date').filter(id = F('listing__realtor_id')).distinct()
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    listings= Listing.objects.all()
    context = {
        'listings': listings,
        'realtors' : realtors,
        'mvp_realtors' : mvp_realtors
    }
    return render(request, 'pages/about.html', context)
