from django.urls import path
from .views import PropertyReviewCreateView, PropertyReviewListView,GuestReviewCreateView,GuestReviewListView

urlpatterns = [
    path('property/reviews/create/', PropertyReviewCreateView.as_view(), name='hotel-review-create'),
    path('properties/<str:property_slug>/reviews/', PropertyReviewListView.as_view(), name='hotel-review-list'),
    path('properties/<str:property_slug>/guest-reviews/', GuestReviewListView.as_view(), name='guest-review-list'),
    path('guests/reviews/create/', GuestReviewCreateView.as_view(), name='guest-review-create'),
   
]