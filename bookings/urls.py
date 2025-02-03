from django.urls import path
from .views import BookingCreateAPIView,BookingCancellationView,UserBookingListView

urlpatterns = [
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('booking/<uuid:booking_id>/cancel/', BookingCancellationView.as_view(), name='booking-cancel'),
    path('bookings/user/', UserBookingListView.as_view(), name='user-booking-list'),
]