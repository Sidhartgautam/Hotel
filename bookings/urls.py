from django.urls import path
from .views import BookingCreateAPIView,BookingCancellationView

urlpatterns = [
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('booking/<uuid:booking_id>/cancel/', BookingCancellationView.as_view(), name='booking-cancel'),
]