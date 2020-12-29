from django.urls import path
from django.contrib.auth import views

from .views import (MainTemplateView, AboutTemplateView, 
                    ContactsTemplateView, ProductsTemplateView,
                    registration)
urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductsTemplateView.as_view(), name='products'),
    path('registration/', registration, name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.LogoutView.as_view(), name='logout'),
]