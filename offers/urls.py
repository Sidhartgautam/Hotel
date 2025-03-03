from django.urls import path
from .views import WeeklyOffersView, AllOffersView

urlpatterns = [
    path('weekly-offers/', WeeklyOffersView.as_view(), name='weekly-offers'),
    path('all-offers/', AllOffersView.as_view(), name='all-offers'),
]
