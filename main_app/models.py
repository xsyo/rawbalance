from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from .utils import img_upload_function


class Profile(models.Model):

    user = models.OneToOneField(get_user_model(), 
                                related_name='profile',
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True
                                )

    fio = models.CharField(max_length=255)
    email = models.EmailField()
    adress = models.TextField()
    phone = PhoneNumberField()

    def __str__(self):
        return self.fio


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to=img_upload_function)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    categoty = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.title