from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from listings.models import Listing
from realtors.models import Realtor as Realtor1
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from realtors.models import Realtor


def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        description=request.POST['description']
        photo=request.FILES.get('photo', False)
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username= username, password= password, email= email, first_name = first_name, last_name= last_name)
                    user.save()
                    realtor1 = Realtor1.objects.create(name=first_name+" "+last_name,photo=photo,description=description,phone=phone,email=email)
                    realtor1.save()
                    messages.success(request, 'You are now registered please log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    listings = Listing.objects.order_by("-list_date").filter(user_id = request.user.id)
    #listing_con = Listing.objects.all().filter(address = F('contact__id'))
    context = {
        'contacts': user_contacts,
        'listings':listings,
    }
    return render(request, 'accounts/dashboard.html', context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Password reset initiated. Check your email."
    success_url = 'login'



def delete(request,list_id):
    instance = Listing.objects.get(id=list_id)
    instance.delete()
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    listings = Listing.objects.order_by("-list_date").filter(user_id = request.user.id)
    context={
        'user_contacts':user_contacts,
        'listings':listings
    }
    return render(request,'accounts/dashboard.html', context)