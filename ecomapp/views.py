from django.shortcuts import render,HttpResponse
from django.views.generic import View, TemplateView
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "about.html"
    
def contact(request):
    if request.method == 'POST': # check post.0 
        name = request.POST['fname']
        phone = request.POST['phone']
        address = request.POST['address']
        msg = request.POST['msg']
        if name!= '' and phone!='' and address!='' and msg!='' :
            contact = ContactMessage(name = name , phone = phone, address = address,message = msg)
            contact.save()
            messages.success(request, 'Your Message Received.We will back you soon')
    return render(request, 'contactus.html')

class AllProductsView(TemplateView):
    template_name = "allproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


def SearchView(request):
    search = request.GET['search']
    if search is not None:
        search = search.replace('#',' ')
        search = search.strip()
    if not search:
        productstitle = Product.objects.none()
        productscontent = Product.objects.none()
    else:
        productstitle = Product.objects.filter(title__icontains=search, available=True)
        productscontent = Product.objects.filter(content__icontains=search, available=True)    
    products = productstitle.union(productscontent)
    params = {'products':products,'search':search}
    return render(request,'search.html',params)

class ProductsDetailView(TemplateView):
    template_name = "productdeatil.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class CategoryDetailView(TemplateView):
    model = Product
    template_name = 'categorydeatil.html'
    order = ['id']
    paginate_by = 8  #and that's it !

    
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView,self).get_context_data(**kwargs)
        categoryID = self.kwargs['cat_id']
        products = None
        products = Product.get_all_products_by_categoryid(categoryID).order_by('id')
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
       
        try:
            page_obj = paginator.get_page(page_number)

        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['allcategories'] = Category.objects.all()
        return context
