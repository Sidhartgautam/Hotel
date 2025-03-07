from rest_framework import serializers
from cloudinary.utils import cloudinary_url
from .models import Property,PropertyImage,PropertyCategory,CancellationPolicy,BreakfastInfo,PropertyAmenities,ParkingInfo,Policy
from reviews.models import PropertyReview
from rooms.models import RoomType
from rooms.serializers import RoomTypeSerializer
from country.models import City
from rooms.models import Price
from django.db.models import Avg
from offers.models import WeeklyOffer
from datetime import date
from datetime import timedelta
from django.db.models import Sum

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
    free_cancellation = serializers.SerializerMethodField()
    best_price = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'property_name', 'short_description', 'city_name', 'rooms',
            'rating', 'review_count', 'images','slug','free_cancellation','best_price'
        ]

        

    def get_rating(self, obj):
        avg_rating = PropertyReview.objects.filter(property_reviewed=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        return PropertyReview.objects.filter(property_reviewed=obj).count()

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None

    def get_city_name(self, obj):
        return obj.city.city_name

    def get_rooms(self, obj):
        check_in = self.context.get('check_in', date.today())  
        check_out = self.context.get('check_out', check_in + timedelta(days=1)) 
        max_guests = self.context.get('max_guests', 1)
        rooms_requested = self.context.get('rooms_requested', 1)

        available_room_types = RoomType.objects.filter(
            property=obj,
            max_no_of_guests__gte=max_guests,
            availabilities__date__gte=check_in,
            availabilities__date__lt=check_out  
        ).annotate(
            total_available=Sum('availabilities__available_rooms')
        ).filter(total_available__gte=rooms_requested).distinct()

        return RoomTypeSerializer(available_room_types, many=True).data
    def get_free_cancellation(self, obj):
        try:
            cancellation_policy = obj.cancellation_policy.first()
            if cancellation_policy and cancellation_policy.cancellations_allowed and cancellation_policy.cancellation_fee_type == 'none':
                return "Free cancellation available"
        except AttributeError:
            return None
        return None
    
    def get_best_price(self, obj):
        if obj.is_single_unit:
            if hasattr(obj, 'single_unit_price') and obj.single_unit_price:
                return obj.single_unit_price.get_effective_price()
            return None

        check_in = self.context.get('check_in', date.today())
        check_out = self.context.get('check_out', check_in + timedelta(days=1))
        max_guests = self.context.get('max_guests', 1)
        rooms_requested = self.context.get('rooms_requested', 1)

        room_query = RoomType.objects.filter(
            property=obj,
            max_no_of_guests__gte=max_guests,
            availabilities__date__gte=check_in,
            availabilities__date__lt=check_out
        ).annotate(
            total_available=Sum('availabilities__available_rooms')
        ).filter(total_available__gte=rooms_requested).distinct()

        if room_query.exists():
            prices = []
            for room in room_query:
                base_price = room.prices.first()  
                if base_price:
                    final_price = base_price.calculate_final_price(num_guests=max_guests)
                    if base_price.is_active() and base_price.is_seasonal:
                        seasonal_discount = base_price.discount_percentage
                        final_price -= (final_price * (seasonal_discount / 100))

                    weekly_offer = WeeklyOffer.objects.filter(
                        property=obj,
                        start_date__lte=date.today(),
                        end_date__gte=date.today()
                    ).first()

                    if weekly_offer and weekly_offer.is_active():
                        offer_discount = weekly_offer.discount_percentage
                        final_price -= (final_price * (offer_discount / 100))

                    prices.append(final_price)
            return min(prices) if prices else None
        return None

    

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
    category = serializers.CharField(source="category.category_name")
    city_name = serializers.CharField(source="city.city_name")
    short_description = serializers.SerializerMethodField()
    rating = serializers.FloatField(source="avg_rating", read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'category', 'property_name', 'short_description', 'city_name',
            'rating', 'review_count', 'images', 'slug'
        ]

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None
    
class PropertyByCategorySerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()

    class Meta:
        model = PropertyCategory
        fields = ['id', 'category_name', 'description', 'properties', 'image']

    def get_properties(self, obj):
        properties = obj.properties.all()
        return PropertySerializer(properties, many=True).data
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            None

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
    single_unit_price = serializers.SerializerMethodField()

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
            'single_unit_price',
            'is_single_unit'
        ]

    def get_facilities(self, obj):
        amenities = obj.amenities.all()[:8]
        return PropertyAmenitiesSerializer(amenities, many=True).data
    
    def get_rating(self, obj):
        avg_rating = PropertyReview.objects.filter(property_reviewed=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        return PropertyReview.objects.filter(property_reviewed=obj).count()
    def get_city_name(self, obj):
        return obj.city.city_name
    def get_single_unit_price(self, obj):
        if obj.is_single_unit:
            if hasattr(obj, 'single_unit_price') and obj.single_unit_price:
                return {
                    "base_price_per_night": obj.single_unit_price.base_price_per_night,
                    "seasonal_price": obj.single_unit_price.seasonal_price,
                    "discount_percentage": obj.single_unit_price.discount_percentage,
                    "currency": obj.single_unit_price.currency.code if obj.single_unit_price.currency else None,
                    "effective_price": obj.single_unit_price.get_effective_price()
                }
            else:
                raise serializers.ValidationError(
                    {"single_unit_price": "Single unit property must have a price set."}
                )
        return None
    
class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            'id', 'property', 'checkin_time_from','checkin_time_to', 'checkout_time_from', 'checkout_time_to',
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
    
class MoredealspropertySerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='property_name')
    banner=serializers.SerializerMethodField()
    open_hrs=serializers.SerializerMethodField()
    user=serializers.CharField(source='user.username')
    class Meta:
        model=Property
        fields=['id','name','address','banner','user','slug','open_hrs']

    def get_open_hrs(self, obj):
        return None
    def get_banner(self, obj):
        image_first = obj.images.first()
        if image_first:
            return image_first.image.url
        return None
    
class PopularPropertySerializer(serializers.ModelSerializer):
    booking_count = serializers.IntegerField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    effective_price = serializers.FloatField(read_only=True)
    popularity_score = serializers.FloatField(read_only=True)
    banner=serializers.SerializerMethodField()
    name=serializers.CharField(source='property_name')

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'address', 'star_rating_property', 'booking_count',
            'review_count', 'effective_price', 'popularity_score', 'slug','banner'
        ]
    def get_banner(self, obj):
        image_first = obj.images.first()
        if image_first:
            return image_first.image.url
        return None