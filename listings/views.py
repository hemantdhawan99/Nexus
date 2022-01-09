from django.contrib import messages
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import listings
from .choices import price_choices, bedroom_choices, state_choices, locations
from .models import Listing
import pandas as pd
import numpy as np
# from matplotlib import pyplot as plt
# import matplotlib
import pickle
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import sklearn.linear_model._base
import json
import os
# file_path = os.path.join(BASE_DIR, 'relative_path')

__model = None
__datacolumns= None
final_res = None


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published = True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request , 'listings/listings.html', context)

def listing(request, listing_id):

    instance = Listing.objects.filter(id=listing_id).values('city')[0]
    city = instance['city']
    location=city
    instance1 = Listing.objects.filter(id=listing_id).values('bedrooms')[0]
    bedrooms = instance1['bedrooms']
    bhk=bedrooms
    instance2 = Listing.objects.filter(id=listing_id).values('bathrooms')[0]
    bathrooms = instance2['bathrooms']
    bath=bathrooms
    instance3 = Listing.objects.filter(id=listing_id).values('sqft')[0]
    sqft = instance3['sqft']
    total_sqft=sqft

    global __datacolumns
    global __model

    with open("models/columns.json",'r') as f:
        __datacolumns = json.load(f)['data_columns']

    with open("models/banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)

    global final_res

    final_res = predict_price(location, bhk, bath, total_sqft)

    listing = get_object_or_404(Listing, pk=listing_id)
    

    context = {
        'listing' : listing,
        'final_res': final_res,
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains = keywords)
        
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact = city)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact = state)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte = bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte = price)


    context ={
        'state_choices' : state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'locations':locations,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)




def predict_price(location,bhk,bath,t_sqft):
    try:    
        loc_index = __datacolumns.index(location.lower())
    except:
        loc_index= -1
    x = np.zeros(len(__datacolumns))
    x[0] = t_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    dat = pd.DataFrame([x], columns=__datacolumns)

    return round(__model.predict(dat)[0],2)

def predict(request):
    
    try:
        if request.method== 'POST':
            location = request.POST['location']
            bhk = request.POST['bhk']
            bath = request.POST['bath']
            t_sqft = request.POST['total_sqft']

            global __datacolumns
            global __model

            with open("models/columns.json",'r') as f:
                __datacolumns = json.load(f)['data_columns']

            with open("models/banglore_home_prices_model.pickle", 'rb') as f:
                __model = pickle.load(f)

            global final_res

            final_res = predict_price(location, bhk, bath, t_sqft)

            context = {
                'location': location,
                'bhk': bhk,
                'bath': bath,
                't_sqft': t_sqft,
                'final_res': final_res,
            }
            return render(request, 'listings/price.html', context)
    except:
        messages.error(request,"Enter all the fields correctly")
        context1= {
        'locations': locations,
        'bedroom_choices' : bedroom_choices,
    }

        return render(request, 'listings/predict.html', context1)


    context= {
        'locations':locations,
        'final_res' : final_res,
        'bedroom_choices' : bedroom_choices,
    }
    return render(request, 'listings/predict.html', context)

def price(request):
    return render(request, 'listings/price.html')