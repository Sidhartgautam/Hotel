from django.urls import path
from .views import (UserPropertyReviewsListView,
                     UserGuestReviewsListView,
                     PropertyReviewCreateView, 
                     PropertyReviewListView,
                     GuestReviewCreateView,
                     GuestReviewListView,
                     CreateCombinedReviewView
)

urlpatterns = [
    path('property/reviews/create/', PropertyReviewCreateView.as_view(), name='hotel-review-create'),
    path('properties/<str:property_slug>/reviews/', PropertyReviewListView.as_view(), name='hotel-review-list'),
    path('properties/<str:property_slug>/guest-reviews/', GuestReviewListView.as_view(), name='guest-review-list'),
    path('guests/reviews/create/', GuestReviewCreateView.as_view(), name='guest-review-create'),
    path('reviews/property/', UserPropertyReviewsListView.as_view(), name='user-property-reviews'),
    path('reviews/facilities/', UserGuestReviewsListView.as_view(), name='user-guest-reviews'),  
    path('combined/reviews/create/', CreateCombinedReviewView.as_view(), name='create-combined-review'),
]