from django.urls import path
from .views import CurrencyListView

urlpatterns = [
    path('currencies/', CurrencyListView.as_view(), name='currency-list'),
]