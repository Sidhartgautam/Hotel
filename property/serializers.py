from rest_framework import serializers
from cloudinary.utils import cloudinary_url
from .models import Property,PropertyImage,PropertyCategory,CancellationPolicy,BreakfastInfo,PropertyAmenities,ParkingInfo,Policy
from reviews.models import PropertyReview
from rooms.models import RoomType
from rooms.serializers import RoomTypeSerializer
from country.models import City
from rooms.models import Price
from django.db.models import Avg, Count

class PropertyCategorySerialzier(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    class Meta:
        model=PropertyCategory
        fields=['id','category_name','image']
    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        return None
class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model=PropertyImage
        fields=['image']
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
class PropertySearchSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'property_name', 'short_description', 'city_name', 'rooms',
            'rating', 'review_count', 'images','slug'
        ]

    def get_rating(self, obj):
        avg_rating = PropertyReview.objects.filter(property=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        return PropertyReview.objects.filter(property=obj).count()

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None

    def get_city_name(self, obj):
        return obj.city.city_name

    def get_rooms(self, obj):
        check_in = self.context.get('check_in')
        check_out = self.context.get('check_out')
        max_guests = self.context.get('max_guests')
        rooms_requested = self.context.get('rooms_requested', 1)

        # Base query for available rooms
        room_query = RoomType.objects.filter(
            property=obj,
            no_of_available_rooms__gte=rooms_requested,
            max_no_of_guests__gte=max_guests
        )

        # Apply date filters only if both check_in and check_out are provided
        if check_in and check_out:
            room_query = room_query.exclude(
                bookings__check_in__lt=check_out,
                bookings__check_out__gt=check_in
            )

        available_rooms = room_query
        return RoomTypeSerializer(available_rooms, many=True).data
    

class TrendingDestinationSerializer(serializers.ModelSerializer):
    average_price = serializers.SerializerMethodField()
    property_count = serializers.IntegerField()  
    image=serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'city_name', 'average_price', 'property_count', 'image'] 
    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        else:
            None

    def get_average_price(self, obj):
        # Calculate the average room price for properties in the city
        avg_price = Price.objects.filter(property__city=obj).aggregate(Avg('base_price_per_night'))['base_price_per_night__avg']
        return round(avg_price, 2) if avg_price else 0
    
class PropertySerializer(serializers.ModelSerializer):
    category=serializers.SerializerMethodField()
    category_description=serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = [
            'id','category','category_description', 'property_name', 'short_description', 'city_name',
            'rating', 'review_count', 'images'
        ]
    def get_category(self,obj):
        return obj.category.category_name
    
    def get_category_description(self,obj):
        return obj.category.description

    def get_rating(self, obj):
        avg_rating = PropertyReview.objects.filter(property=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        return PropertyReview.objects.filter(property=obj).count()

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None

    def get_city_name(self, obj):
        return obj.city.city_name

class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = [
            'property', 'cancellations_allowed', 'cancellation_deadline_days', 
            'cancellation_fee_type', 'cancellation_fee_amount', 'refundable', 
            'additional_notes'
        ]
        read_only_fields = ['property']

    def validate(self, data):
        if data.get('cancellation_fee_type') == 'percentage' and data.get('cancellation_fee_amount'):
            if data['cancellation_fee_amount'] > 100 or data['cancellation_fee_amount'] < 0:
                raise serializers.ValidationError("Percentage fee must be between 0 and 100.")
        if data.get('cancellation_fee_type') == 'fixed' and data.get('cancellation_fee_amount', 0) < 0:
            raise serializers.ValidationError("Fixed cancellation fee must be non-negative.")
        return data

class BreakfastInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakfastInfo
        fields = ['serve_breakfast', 'breakfast_included', 'breakfast_type', 'extra_cost']

class ParkingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingInfo
        fields = ['parking_availability', 'parking_price', 'reservation_required', 'parking_location', 'parking_access']

class PropertyAmenitiesSerializer(serializers.ModelSerializer):
    amenity_name = serializers.CharField(source="amenity.name")  

    class Meta:
        model = PropertyAmenities
        fields = ['amenity_name', 'is_available']
class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Property
        fields=['property_name','address','star_rating_property','city','lat','lng','images','description','facilities','breakfast_info','parking_info','review_count','rating','slug']

class PropertyDetailsSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True) 
    breakfast_info = BreakfastInfoSerializer(many=True, read_only=True) 
    parking_info = ParkingInfoSerializer(many=True, read_only=True)
    facilities = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    city_name=serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id',
            'property_name',
            'address',
            'star_rating_property',
            'city_name',
            'lat',
            'lng',
            'images',
            'description',
            'facilities',
            'breakfast_info',
            'parking_info',
            'review_count',
            'rating',
            'slug',
        ]

    def get_facilities(self, obj):
        amenities = obj.amenities.all()[:8]
        return PropertyAmenitiesSerializer(amenities, many=True).data
    
    def get_rating(self, obj):
        avg_rating = PropertyReview.objects.filter(property=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        return PropertyReview.objects.filter(property=obj).count()
    def get_city_name(self, obj):
        return obj.city.city_name
    
class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            'id', 'property', 'checkin_time', 'checkout_time',
            'children_allowed', 'extra_beds_available', 'extra_bed_cost',
            'pets_allowed', 'pet_fee', 'pet_details'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('extra_beds_available') and not data.get('extra_bed_cost'):
            raise serializers.ValidationError({"extra_bed_cost": "Extra bed cost is required if extra beds are available."})

        if data.get('pets_allowed') and (not data.get('pet_fee') or not data.get('pet_details')):
            raise serializers.ValidationError({
                "pet_fee": "Pet fee is required if pets are allowed.",
                "pet_details": "Pet details are required if pets are allowed."
            })
        return data