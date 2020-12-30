from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import Product, Category, Profile
from .forms import RegistrationForm


class MainTemplateView(ListView):

    template_name = 'main/index.html'
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()[:9]
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class AboutTemplateView(TemplateView):

    template_name = 'main/about.html'


class ContactsTemplateView(TemplateView):

    template_name = 'main/contacts.html'


class ProductsTemplateView(ListView):

    template_name = 'main/products.html'
    context_object_name = 'products'
    model = Product
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


def registration(request):
    
    if request.method == 'POST':

        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            User = get_user_model()
          
            user = User.objects.create_user(registrationForm.cleaned_data['email'],
                                            registrationForm.cleaned_data['email'],
                                            registrationForm.cleaned_data['password'])

            profile = Profile(user=user,
                              fio=registrationForm.cleaned_data['fio'],
                              email=registrationForm.cleaned_data['email'],
                              adress=registrationForm.cleaned_data['adress'])
            profile.save()
            return redirect('login')
    else:
        registrationForm = RegistrationForm()
    return render(request, 'main/registration.html', {'form': registrationForm})

