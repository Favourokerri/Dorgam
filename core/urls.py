from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('signUp', views.signUp, name="signUp"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('editProfile', views.edit_profile_page, name="editProfile"),
    path('profile', views.profile_page, name="profile"),
    path('about', views.about_page, name="about"),
    path('services', views.services, name="services"),
    path('service/<int:id>/', views.single_service, name="service"),
    path('bookService', views.book_service, name="bookService"),
    path('contactUs', views.contact_us, name="contactUs"),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('subscribe', views.subscribe, name="subscribe"),

]
