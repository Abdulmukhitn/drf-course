from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views



urlpatterns = [
    path('products/', views.product_list, name='product-list'),
]

