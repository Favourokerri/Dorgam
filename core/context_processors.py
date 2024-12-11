from django.shortcuts import render
from .models import Contact

# Create your views here.
def contact_info(request):
    contactInfo = Contact.objects.first()
    return {"contact": contactInfo}