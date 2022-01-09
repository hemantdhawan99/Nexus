from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from realtors.models import Realtor as Realtor1

from listings.choices import state_choices, locations,rera
from listings.models import Listing

def addlisting(request):        
    context= {
        'state_choices': state_choices,
        'locations': locations,
        'rera':rera
    }
    return render(request,'addlisting/addlisting.html', context)


def listing_sub(request):
    realtor=Realtor1.objects.all()
    realtor_instance=Realtor1.objects.get(name=request.user.first_name+" "+request.user.last_name)
    
    if request.method=='POST':
        realtor=realtor_instance
        rera_approved = request.POST['rera_approved']
        upload_doc= request.FILES.get('upload_doc', False)
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        zipcode=request.POST['zipcode']
        description=request.POST['description']
        price=request.POST['price']
        bedrooms=request.POST['bedrooms']
        bathrooms=request.POST['bathrooms']
        garage=request.POST['garage']
        sqft=request.POST['sqft']
        lot_size=request.POST['lot_size']
        photo_main=request.FILES['photo_main']
        photo_1=request.FILES.get('photo_1', False)
        photo_2=request.FILES.get('photo_2', False)
        photo_3=request.FILES.get('photo_3', False)
        photo_4=request.FILES.get('photo_4', False)
        photo_5=request.FILES.get('photo_5', False)
        photo_6=request.FILES.get('photo_6', False)
        list_date=request.POST['list_date']

        if request.user.is_authenticated:
            user_id = request.user.id
            listing1 = Listing.objects.create(realtor=realtor_instance,address=address,city=city,state=state,zipcode=zipcode,description=description,price=price,bedrooms=bedrooms,bathrooms=bathrooms,garage=garage,sqft=sqft,lot_size=lot_size,photo_main=photo_main,photo_1=photo_1,photo_2=photo_2,photo_3=photo_3,photo_4=photo_4,photo_5=photo_5,photo_6=photo_6,list_date=list_date,upload_doc=upload_doc,rera_approved=rera_approved,user_id=user_id)
                
            listing1.save()
            messages.success(request, 'Listing has been added successfully!')
            return render(request,'accounts/dashboard.html')
    # except:
    #     messages.error(request, 'Something went wrong!')
    #     return render(request,'addlisting/addlisting.html')
