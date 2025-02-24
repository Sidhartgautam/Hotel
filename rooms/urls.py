from django.urls import path
from .views import PropertyRoomListView,RoomDetailsView,RoomAmenitiesView

urlpatterns = [
    path('property/<str:property_slug>/rooms/', PropertyRoomListView.as_view(), name='property-room-list'),
    path('property/<str:property_slug>/rooms/<uuid:id>/', RoomDetailsView.as_view(), name='room-details'),
    path('rooms/<uuid:id>/amenities/', RoomAmenitiesView.as_view(), name='room-amenities'),
]
