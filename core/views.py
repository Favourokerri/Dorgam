from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, HttpResponse
from .models import HeroSection, About, Service, BookedService, Lead, ContactUs
from .functions import send_booking_email_to_client, send_booking_email_to_admin, addToLead
from ecommerceShop.models import Product
from .functions import contact_email_to_admin

def signUp(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("LastName")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.create_user(
                username=email, 
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        
        except IntegrityError:
            messages.error(request, "A user with this email already exists.")
            return render(request, "mainSite/signUpPage.html")
    return render(request, "mainSite/signUpPage.html")

def login(request):
    return render(request, "mainSite/loginPage.html")

def home_page(request):
    heroContent = HeroSection.objects.first()
    services = Service.objects.all()
    featured_products = Product.objects.filter(is_featured=True)
    
    context = {'heroContent': heroContent,
               'services': services,
               'featured_products': featured_products
               }

    return render(request, "mainSite/homePage.html", context)

def about_page(request):
    about = About.objects.first()

    context = {'about': about}
    return render(request, "mainSite/aboutPage.html", context)

def services(request):
    search_query = request.GET.get('q', '') 
    
    if search_query:
        services = Service.objects.filter(name_of_service__icontains=search_query)
    else:
        services = Service.objects.all()

    context = {'services': services, 'search_query': search_query}
    return render(request, "mainSite/servicesPage.html", context)

def book_service(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('fullName')
            phone_number = request.POST.get('phoneNumber')
            email = request.POST.get('email')
            best_time = request.POST.get('bestTime')
            contact_method = request.POST.get('contactMethod')
            service_name = request.POST.get('service')
            notes = request.POST.get('notes')

            booking = BookedService.objects.create(
                fullName=full_name,
                phoneNumber=phone_number,
                email=email,
                time_to_contact=best_time,
                preferred_contact_method=contact_method,
                service=service_name,
                additional_notes=notes or ""
            )

            addToLead(full_name, email)
            try:
                send_booking_email_to_client(request, full_name, email, service_name,
                                         contact_method, best_time)
                send_booking_email_to_admin(
                    request, full_name, phone_number, email, service_name,
                    contact_method, best_time, notes)
                print("sent")
            except Exception as e:
                print(e)
        
            messages.success(request, "service booked successfully")
            return redirect('services')
        except Exception as e:
            print(e)

    services = Service.objects.all()
    context = {'services': services}
    return render(request, "mainSite/bookServicePage.html", context)

def unsubscribe(request, email):
    """
    Deletes the email from the Lead model, effectively unsubscribing the user.
    """
    try:
        lead = Lead.objects.filter(email=email).first()
        if lead:
            lead.delete()
            messages.success(request, 'You have successfully unsubscribed from our mailing list.')
        else:
            messages.warning(request, 'This email is already unsubscribed or not found in our records.')
    except Exception as e:
        print(f"Error during unsubscribe: {e}")
        return HttpResponse("An unexpected error occurred. Please try again later.", status=500)
    return redirect(home_page)

def contact_us(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            ContactUs.objects.create(name=name, email=email, message=message)
            contact_email_to_admin(request, name, email, message)
            messages.success(request, "message sent successfully")
            return redirect('contactUs')
        except Exception as e:
            messages.error(request, "sorry some error occured. try again later")
            print(e)
        
    return render(request, "mainSite/contactPage.html")