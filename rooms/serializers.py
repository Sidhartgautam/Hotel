from rest_framework import serializers
from .models import RoomType,BedType
class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            'id', 'room_type', 'room_name', 'no_of_available_rooms',
            'max_no_of_guests', 'room_size', 'smoking_allowed'
        ]

class BedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=BedType
        fields=[
            'id','bed_type'
        ]

