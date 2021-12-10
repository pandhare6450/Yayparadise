from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.http import request
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from ecomproject.utils import unique_slug_generator

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.CharField(max_length=100,null=True, blank=True)
    image=models.ImageField(upload_to="products",null=True, blank=True)

    class Meta:
        unique_together = ("title", "content" )


    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    anyoffers =  models.BooleanField(default=False)
    offers = models.CharField(max_length=100,null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to="products",null=True, blank=True)
    family = models.CharField(max_length=200,null=True, blank=True)
    uses = models.CharField(max_length=200,null=True, blank=True)
    soil = models.CharField(max_length=300, null=True, blank=True)
    fertiliser = models.CharField(max_length=300, null=True, blank=True)
    water=models.CharField(max_length=200,null=True)
    view_count = models.PositiveIntegerField(default=0)
    
    
    class Meta:
        unique_together = ("title", "category", )

    def __str__(self):
        return self.title

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.filter(available=True)

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        return Product.objects.filter(category = category_id,available=True)

    @staticmethod
    def get_all_products_by_offers():
        return Product.objects.filter(anyoffers=True,available=True)
        
        
class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    
    name= models.CharField(blank=True,max_length=20)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    address = models.CharField(blank=True, max_length=90)
    phone = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "phone", )

    def __str__(self):
        return self.name    



def slug_genertor(sender,instance,*args,**kwrgs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    return

pre_save.connect(slug_genertor,sender=Product)
pre_save.connect(slug_genertor,sender=Category)