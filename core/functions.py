from django.core.mail import EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import Lead

def addToLead(fullName, email):
    if Lead.objects.filter(email=email).exists():
        return
    is_user = User.objects.filter(email=email).exists()

    Lead.objects.create(
        fullName=fullName,
        email=email,
        is_user=is_user
    )

def send_booking_email_to_client(request, full_name, email, service_name, preferred_contact_method, time_to_contact):
    unsubscribe_url = request.build_absolute_uri(
        reverse('unsubscribe', args=[email])
    )
    # Render the email template
    email_body = render_to_string('emails/booking_confirmation.html', {
        'full_name': full_name,
        'email': email,
        'service_name': service_name,
        'preferred_contact_method': preferred_contact_method,
        'time_to_contact': time_to_contact,
        'unsubscribe_url': unsubscribe_url,
    })

    # Create email
    email_message = EmailMessage(
        subject='Booking Confirmation',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email_message.content_subtype = 'html'
    email_message.send()

def send_booking_email_to_admin(request, full_name, phone_number, email, 
                                service_name, preferred_contact_method, 
                                time_to_contact, additional_notes):
    unsubscribe_url = request.build_absolute_uri(
        reverse('unsubscribe', args=[email])
    )
    
    admins = User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True)

    if not admins:
        print("No admin emails found.")
        return
    
    email_body = render_to_string('emails/admin_booking_notification.html', {
        'full_name': full_name,
        'phone_number': phone_number,
        'email': email,
        'service_name': service_name,
        'preferred_contact_method': preferred_contact_method,
        'time_to_contact': time_to_contact,
        'additional_notes': additional_notes,
         'unsubscribe_url': unsubscribe_url,
    })

    # Create the email
    email_message = EmailMessage(
        subject='New Booking Notification',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(admins),
    )
    email_message.content_subtype = 'html'

    try:
        email_message.send()
    except Exception as e:
        print(f"Error sending email to admins: {e}")


def contact_email_to_admin(request, name, email, message):
    admins = User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True)

    if not admins:
        print("No admin emails found.")
        return
    
    email_body = render_to_string('emails/contact_admin_notification.html', {
        'name': name,
        'email': email,
        'message': message,
    })

    # Create the email
    email_message = EmailMessage(
        subject='Client Reaching Out',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(admins),
    )
    email_message.content_subtype = 'html'

    try:
        email_message.send()
    except Exception as e:
        print(f"Error sending email to admins: {e}")