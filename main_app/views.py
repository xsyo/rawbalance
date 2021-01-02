from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

from .models import Product, Category, Profile, Order
from .forms import RegistrationForm, ProfileForm


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


def ordering_process(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        order = Order(customer=request.user.profile,
                      product=product)
        
        order.save()

        return redirect('payment_process', order_id=order.id) # страница оплаты
    
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save()
            order = Order(customer=profile,
                      product=product)            
            order.save()

            return redirect('payment_process', order_id=order.id) # страница оплаты
    else:
        form = ProfileForm()
    
    return render(request, 'main/ordering_process.html', {'form': form})


def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.get_price(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'custom': str(order.customer.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'main/payment_process.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'main/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment_cancelled.html')