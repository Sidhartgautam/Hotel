from rest_framework import serializers
from .models import RoomType,BedType,RoomAmenities,RoomImages,RoomBed,RoomAvailability
import random
from django.db import models
from django.db.models import Sum
from datetime import date
class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            'id', 'room_type', 'room_name',
            'max_no_of_guests', 'room_size', 'smoking_allowed'
        ]
class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
        fields = ['id', 'room_type', 'date', 'available_rooms']

class RoomImageSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    class Meta:
        model=RoomImages
        fields=['image']
    def get_image(self,obj):
        return obj.image.url

class RoomAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenities
        fields = '__all__'

    def to_representation(self, instance):
        amenities = {
            field.name: getattr(instance, field.name)
            for field in self.Meta.model._meta.get_fields()
            if isinstance(field, models.BooleanField) and getattr(instance, field.name)
        }
        # print("amenities",amenities)
        selected_amenities = random.sample(list(amenities.items()), min(5, len(amenities)))
        
        return {key: True for key, value in selected_amenities}

class RoomSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='get_room_type_display')
    available_rooms = serializers.SerializerMethodField()
    price_per_night = serializers.SerializerMethodField()
    offer_price = serializers.SerializerMethodField()
    seasonal_price = serializers.SerializerMethodField()
    room_amenities=RoomAmenitiesSerializer(source='all_room_amenities',many=True,read_only=True)
    room_images=RoomImageSerializer(many=True, source='images')

    class Meta:
        model = RoomType
        fields = [
            'id',
            'room_type_name', 
            'available_rooms', 
            'price_per_night', 
            'offer_price', 
            'seasonal_price', 
            'room_amenities',
            'room_images'
        ]

    def get_price_per_night(self, obj):
        price = obj.prices.filter(is_seasonal=False).first()
        return price.base_price_per_night if price else None
    
    def get_available_rooms(self, obj):
        check_in = self.context.get('check_in', date.today())
        check_out = self.context.get('check_out')

        if check_out:
            available_rooms = RoomAvailability.objects.filter(
                room_type=obj,
                date__gte=check_in,
                date__lt=check_out
            ).aggregate(total=Sum('available_rooms'))['total']
        else:
            available_rooms = RoomAvailability.objects.filter(
                room_type=obj,
                date=check_in 
            ).aggregate(total=Sum('available_rooms'))['total']

        return available_rooms or 0

    def get_offer_price(self, obj):
        offer = obj.property.weekly_offers.filter(
            start_date__lte=date.today(), 
            end_date__gte=date.today()
        ).first()
        if offer:
            base_price = self.get_price_per_night(obj)
            if base_price:
                discount_amount = base_price * (offer.discount_percentage / 100)
                return round(base_price - discount_amount, 2)
        return None

    def get_seasonal_price(self, obj):
        seasonal_price = obj.prices.filter(
            is_seasonal=True, 
            start_date__lte=date.today(), 
            end_date__gte=date.today()
        ).first()
        return seasonal_price.base_price_per_night if seasonal_price else None


    
class AllRoomAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenities
        fields = '__all__' 

    def to_representation(self, instance):
        amenities = {
            field.name: getattr(instance, field.name)
            for field in self.Meta.model._meta.get_fields()
            if isinstance(field, models.BooleanField) and getattr(instance, field.name)
        }
        selected_amenities = list(amenities.items())
        
        return {key: True for key, value in selected_amenities}

class RoomBedSerializer(serializers.ModelSerializer):
    bed_type_name = serializers.CharField(source='bed_type.get_bed_type_display')  # Use get_bed_type_display

    class Meta:
        model = RoomBed
        fields = ['bed_type_name', 'quantity']

class RoomDetailsSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, source='images')
    room_amenities=AllRoomAmenitiesSerializer(source='all_room_amenities',many=True,read_only=True)
    room_beds = RoomBedSerializer(many=True) 
    extra_guest_price = serializers.SerializerMethodField()
    extra_breakfast_cost = serializers.SerializerMethodField()
    extra_parking_cost = serializers.SerializerMethodField()

    class Meta:
        model = RoomType
        fields = [
            'id',
            'room_images',
            'room_amenities',
            'room_size',
            'smoking_allowed',
            'room_beds',
            'extra_guest_price',
            'extra_breakfast_cost',
            'extra_parking_cost',
            'max_no_of_guests',
        ]

    def get_price_instance(self, obj):
        """Retrieve the first active price for the room."""
        return obj.prices.filter(is_seasonal=False).first()

    def get_extra_guest_price(self, obj):
        price = self.get_price_instance(obj)
        return price.extra_guest_price if price and price.extra_guest_price > 0 else None

    def get_extra_breakfast_cost(self, obj):
        price = self.get_price_instance(obj)
        if price:
            return price.breakfast_price if price.breakfast_price > 0 else "Included"
        return "Included"

    def get_extra_parking_cost(self, obj):
        price = self.get_price_instance(obj)
        if price:
            return price.parking_price if price.parking_price > 0 else "Included"
        return "Included"



