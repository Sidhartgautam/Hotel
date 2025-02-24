from rest_framework import generics, permissions, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import RoomType,RoomAmenities
from property.models import Property
from .serializers import RoomSerializer,RoomDetailsSerializer,RoomAmenitiesSerializer
from core.utils.response import PrepareResponse  # Assuming PrepareResponse is in utils

class PropertyRoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return RoomType.objects.none()
        return RoomType.objects.filter(property=property_instance).select_related('room_amenities')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return PrepareResponse(
                success=True,
                message="Rooms retrieved successfully.",
                data=paginated_response
            ).send(code=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Rooms retrieved successfully.",
            data=serializer.data
        ).send(code=status.HTTP_200_OK)
    

class RoomDetailsView(generics.RetrieveAPIView):
    serializer_class = RoomDetailsSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')
        try:
            from property.models import Property 
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return RoomType.objects.none()
        return RoomType.objects.filter(property=property_instance)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return PrepareResponse(
                success=True,
                message="Room details retrieved successfully.",
                data=serializer.data
            ).send(code=status.HTTP_200_OK)
        except RoomType.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Room not found.",
                data={}
            ).send(code=status.HTTP_404_NOT_FOUND)
        

class RoomAmenitiesView(generics.RetrieveAPIView):  # Use RetrieveAPIView for a single object
    serializer_class = RoomAmenitiesSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'  # This should match the RoomAmenities ID, not RoomType ID

    def get_object(self):
        """Fetch the RoomAmenities object linked to the given RoomType ID."""
        room_type_id = self.kwargs.get('id')  # Get the room type ID from the URL
        try:
            room = RoomType.objects.get(id=room_type_id)  # Fetch the room
            if room.room_amenities:  # Ensure amenities exist
                return room.room_amenities
            else:
                raise RoomAmenities.DoesNotExist  # Raise an error if missing
        except (RoomType.DoesNotExist, RoomAmenities.DoesNotExist):
            raise serializers.ValidationError("No amenities found for this room.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return PrepareResponse(
            success=True,
            message="Room amenities retrieved successfully.",
            data=serializer.data
        ).send(code=status.HTTP_200_OK)

        
