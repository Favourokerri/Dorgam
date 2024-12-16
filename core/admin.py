from django.contrib import admin
from .models import HeroSection, Contact, About, Service
from .models import BookedService, Lead, EmailCampaign, ContactUs, UserProfile, SocialMedia


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'address', 'phone_number')
    ordering = ['user__username']
    search_fields = ('user__username', 'phone_number', 'state')

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Contact)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('address', 'phoneNumber', 'email')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_of_service',)
    search_fields = ('name_of_service',)

@admin.register(BookedService)
class serviceBookedAdmin(admin.ModelAdmin):
    list_display = ('fullName', 'phoneNumber', 'email', 'time_to_contact',
                    'preferred_contact_method', 'status')
    ordering = ['-created_at']
    list_filter = ('status',)
    search_fields = ('fullName', 'email', 'phoneNumber')

@admin.register(Lead)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ('fullName', 'email', 'is_user')
    ordering = ['-created_at']
    list_filter = ('is_user',)
    search_fields = ('fullName', 'email')

@admin.register(ContactUs)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    ordering = ['-created_at']
    list_filter = ('status',)
    search_fields = ('name', 'email')

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'created_at', 'updated_at')
    list_filter = ('audience',)
    search_fields = ('title', 'audience')

admin.site.register(About)
admin.site.register(SocialMedia)
