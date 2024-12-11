from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('signUp', views.signUp, name="signUp"),
    path('login', views.login, name="login"),
    path('about', views.about_page, name="about"),
    path('services', views.services, name="services"),
    path('bookService', views.book_service, name="bookService"),
    path('contactUs', views.contact_us, name="contactUs"),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),

]
