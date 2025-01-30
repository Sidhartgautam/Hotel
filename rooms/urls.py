from django.urls import path
from .views import PropertyRoomListView,RoomDetailsView

urlpatterns = [
    path('property/<str:hotel_slug>/rooms/', PropertyRoomListView.as_view(), name='hotel-room-list'),
    path('property/<str:property_slug>/rooms/<uuid:id>/', RoomDetailsView.as_view(), name='room-details'),
]
