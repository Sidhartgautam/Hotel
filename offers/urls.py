from django.urls import path
from .views import WeeklyOffersView

urlpatterns = [
    path('weekly-offers/', WeeklyOffersView.as_view(), name='weekly-offers'),
]
