from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
class HeroSection(models.Model):
    """ Model for hero section"""
    title = models.CharField(max_length=200, help_text="title for hero section")
    description = models.TextField(max_length=500, help_text="short describtion for website")

    def __str__(self):
        return self.title

class About(models.Model):
    """Model for about page """
    about = CKEditor5Field(config_name='default')

    def __str__(self):
        return "About Dorgam"

class Contact(models.Model):
    address = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=20)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    message = models.TextField()
    STATUS = [
        ('pending', 'pending'),
        ('resolved', 'resolved'),
    ]
    status = models.CharField(max_length=100, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
class Service(models.Model):
    image = models.ImageField(
        upload_to='services/images/',
        blank=False, 
        null=False, 
        help_text="enter service image"
    )
    name_of_service = models.CharField(max_length=200, blank=False, null=False)
    detail = CKEditor5Field(config_name='default')

class BookedService(models.Model):
    fullName = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    CONTACT_METHOD_CHOICES = [
        ('phone call', 'Phone call'),
        ('email', 'Email'),
        ('WhatsApp', 'WhatsApp'),
    ]
    STATUS = [
        ('pending', 'pending'),
        ('waiting on client response', 'waiting on client response'),
        ('resolved', 'resolved'),
    ]

    time_to_contact = models.CharField(max_length=20, choices=TIME_CHOICES, default='morning'
    )

    preferred_contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES,
        default='email'
    )

    service = models.CharField(max_length=200)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Lead(models.Model):
    """ emails of potential leads"""
    fullName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    is_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class EmailCampaign(models.Model):
    AUDIENCE_CHOICES = [
    ('all', 'All Leads'),
    ('users', 'Users'),
    ('non_users', 'Non-Users'),
    ]
    title = models.CharField(max_length=255)
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='all')
    body = CKEditor5Field(config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def send_email(self, request):
        """ Method to send email after saving the campaign """
        try:
            if self.audience == 'all':
                leads = Lead.objects.all()
            elif self.audience == 'users':
                leads = Lead.objects.filter(is_user=True)
            elif self.audience == 'non_users':
                leads = Lead.objects.filter(is_user=False)
            else:
                raise ValueError("Invalid audience selected in the campaign.")

            if not leads.exists():
                raise ValueError("No leads found for the selected audience.")

            from_email = settings.DEFAULT_FROM_EMAIL

            for lead in leads:
                unsubscribe_url = request.build_absolute_uri(
                    reverse('unsubscribe', args=[lead.email])
                )

                # Render the email body with unsubscribe URL
                email_body = render_to_string('emails/campaign_email.html', {
                    'body': self.body,
                    'unsubscribe_url': unsubscribe_url,
                    'full_name': lead.fullName,  # Optional: personalize with lead's name
                })

                email_message = EmailMessage(
                    subject=self.title,
                    body=email_body,
                    from_email=from_email,
                    to=[lead.email],  # Send one email per lead
                )
                email_message.content_subtype = 'html'  # Ensure the email is sent as HTML
                email_message.send()

        except Exception as e:
            print(f"Error while sending email: {e}")
            raise
    
@receiver(post_save, sender=EmailCampaign)
def send_campaign_email(sender, instance, created, **kwargs):
    """ Signal to automatically send the email after saving the campaign """
    from django.http import HttpRequest  # Ensure we have access to a request object

    # Create a dummy request object for generating unsubscribe URLs
    request = HttpRequest()
    request.META['HTTP_HOST'] = settings.SITE_DOMAIN  # Set the domain for absolute URLs

    instance.send_email(request)

class SocialMedia(models.Model):
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"social media"