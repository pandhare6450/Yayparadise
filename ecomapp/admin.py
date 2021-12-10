from django.contrib import admin
from .models import *
from django.utils.html import format_html
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth

admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
   list_display = ['name','less_content', 'create_at', 'update_at','status']
   readonly_fields =('name','message')
   list_filter = ['status','create_at']
   save_on_top = True
   list_per_page = 6
   search_fields = ['name']

   def less_content(self,obj):
      return obj.message[0:10]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   readonly_fields = ['Image_thumb',]
   list_display = ['title','img']
   list_filter = ['title']
   readonly_fields = ('slug',)
   save_on_top = True
   list_per_page = 4
   search_fields = ['title']

   def Image_thumb(self,obj):
      return format_html(f'<img src="/media/{obj.image}" style="width:150px;height:100px">')

   def img(self,obj):
      return format_html(f'<img src="/media/{obj.image}" style="width:50px;height:50px">')

   


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   readonly_fields = ['imgb','slug',]
   list_display = ['title','category','img','anyoffers','available']
   list_filter = ['category','available',('offers',admin.EmptyFieldListFilter)]
   save_on_top = True
   list_per_page = 6
   search_fields = ['title']
   actions = ['make_Available','make_Unavailable']

   def imgb(self,obj):
      return format_html(f'<img src="/media/{obj.image}" style="width:250px;height:250px">')

   def img(self,obj):
      return format_html(f'<img src="/media/{obj.image}" style="width:50px;height:50px">')

   def make_Available(self, request, queryset):
      queryset.update(available=True)
      return
   
   def make_Unavailable(self, request, queryset):
      queryset.update(available=False)
      return