from django.urls import path
from django.contrib.auth import views

from .views import (MainTemplateView, AboutTemplateView, 
                    ContactsTemplateView, ProductsTemplateView,
                    registration, ordering_process, payment_process,
                    payment_done, payment_canceled)
urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductsTemplateView.as_view(), name='products'),

    path('registration/', registration, name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('ordering_process/<int:product_id>/', ordering_process, name='ordering_process'),

    path('payment_process/<int:order_id>/', payment_process, name='payment_process'),

    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),

]