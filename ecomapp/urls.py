from django.urls import path
from .views import *



app_name = "ecomapp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact", contact, name="contact"),
    path("search/", SearchView, name="search"),
    path("all-products/", AllProductsView.as_view(),name="allproducts"),
    path("products/<slug:slug>/", ProductsDetailView.as_view(),name="productdetail"),
    path("category-<slug:cat_id>/",CategoryDetailView.as_view(),name="categorydeatil"),
    
    

    
]
