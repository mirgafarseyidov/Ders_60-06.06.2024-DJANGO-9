from django.urls import path
from .views import portfolio_create

urlpatterns = [
    path('create/', portfolio_create, name='portfolio_create'),
]