from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
]

urlpatterns += router.urls