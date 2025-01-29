from django.urls import path
from .views import PropertyReviewCreateView, HotelReviewListView,GuestReviewCreateView,GuestReviewListView

urlpatterns = [
    path('hotels/reviews/', PropertyReviewCreateView.as_view(), name='hotel-review-create'),
    path('hotels/reviews/list/', HotelReviewListView.as_view(), name='hotel-review-list'),
    path('guests/reviews/', GuestReviewCreateView.as_view(), name='guest-review-create'),
    path('guests/reviews/list/', GuestReviewListView.as_view(), name='guest-review-list'),
   
]