from rest_framework import serializers
from property.models import Property,ParkingInfo,BreakfastInfo,Amenity,PropertyAmenities,PropertyImage,Policy,CancellationPolicy,SingleUnitPrice
from rooms.models import RoomAmenities,RoomType,RoomBed,Price,RoomImages
from offers.models import WeeklyOffer
from faq.models import PropertyFAQ

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'property_name', 'address', 'description', 'star_rating_property',
            'country', 'currency', 'city', 'state', 'lng', 'lat', 'user', 'category', 'language','is_single_unit'
        ]
        read_only_fields = ['id']
    def update(self, instance, validated_data):
        instance.property_name = validated_data.get('property_name', instance.property_name)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.star_rating_property = validated_data.get('star_rating_property', instance.star_rating_property)
        instance.country = validated_data.get('country', instance.country)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.user = validated_data.get('user', instance.user)
        instance.category = validated_data.get('category', instance.category)
        instance.language = validated_data.get('language', instance.language)
        instance.is_single_unit = validated_data.get('is_single_unit', instance.is_single_unit)
        instance.save()
        return instance

class ParkingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingInfo
        fields = [
            'property', 'parking_availability', 'parking_price', 'reservation_required',
            'parking_location', 'parking_access'
        ]
    def update(self, instance, validated_data):
        instance.property = validated_data.get('property', instance.property)
        instance.parking_availability = validated_data.get('parking_availability', instance.parking_availability)
        instance.parking_price = validated_data.get('parking_price', instance.parking_price)
        instance.reservation_required = validated_data.get('reservation_required', instance.reservation_required)
        instance.parking_location = validated_data.get('parking_location', instance.parking_location)
        instance.parking_access = validated_data.get('parking_access', instance.parking_access)
        instance.save()
        return instance

class SingleUnitPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleUnitPrice
        fields = ['property', 'base_price_per_night', 'seasonal_price', 'discount_percentage']
        read_only_fields = ['property']
    def update(self, instance, validated_data):
        instance.property = validated_data.get('property', instance.property)
        instance.base_price_per_night = validated_data.get('base_price_per_night', instance.base_price_per_night)
        instance.seasonal_price = validated_data.get('seasonal_price', instance.seasonal_price)
        instance.discount_percentage = validated_data.get('discount_percentage', instance.discount_percentage)
        instance.save()
        return instance
    
    
class BreakfastInfoSerializer(serializers.ModelSerializer):
    breakfast_type = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                ('continental', 'Continental'),
                ('american', 'American'),
                ('buffet', 'Buffet'),
                ('english', 'English'),
                ('vegetarian', 'Vegetarian'),
                ('vegan', 'Vegan'),
                ('gluten_free', 'Gluten-Free'),
            ]
        ),
        allow_empty=True,
        required=False,
        help_text="List of breakfast types served (e.g., ['continental', 'vegan'])"
    )

    class Meta:
        model = BreakfastInfo
        fields = ['property', 'serve_breakfast', 'breakfast_included', 'breakfast_type', 'extra_cost']
    def update(self, instance, validated_data):
        instance.property = validated_data.get('property', instance.property)
        instance.serve_breakfast = validated_data.get('serve_breakfast', instance.serve_breakfast)
        instance.breakfast_included = validated_data.get('breakfast_included', instance.breakfast_included)
        instance.breakfast_type = validated_data.get('breakfast_type', instance.breakfast_type)
        instance.extra_cost = validated_data.get('extra_cost', instance.extra_cost)
        instance.save()
        return instance

class PropertyAmenityItemSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all())

    class Meta:
        model = PropertyAmenities
        fields = ['amenity', 'is_available']

    def create(self, validated_data):
        # This method is not directly used because we handle bulk creation in the parent serializer.
        pass


class BulkPropertyAmenitiesSerializer(serializers.Serializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    amenities = PropertyAmenityItemSerializer(many=True)

    def create(self, validated_data):
        property_instance = validated_data['property']
        amenities_data = validated_data['amenities']
        property_amenities = []

        for amenity_data in amenities_data:
            amenity_instance = amenity_data.pop('amenity')
            property_amenities.append(
                PropertyAmenities(property=property_instance, amenity=amenity_instance, **amenity_data)
            )
        return PropertyAmenities.objects.bulk_create(property_amenities)
    
class PropertyAmenityUpdateSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), required=False)
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False)

    class Meta:
        model = PropertyAmenities
        fields = ['amenity', 'property', 'is_available']
        read_only_fields = ['amenity', 'property']

    def update(self, instance, validated_data):
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.save()
        return instance
    

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['property', 'image']


class BulkPropertyImageSerializer(serializers.Serializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(),
        help_text="List of image files to upload"
    )

    def create(self, validated_data):
        property_instance = validated_data['property']
        images = validated_data['images']
        property_images = [PropertyImage(property=property_instance, image=image) for image in images]
        return PropertyImage.objects.bulk_create(property_images)

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            'property', 'checkin_time', 'checkout_time', 'children_allowed',
            'extra_beds_available', 'extra_bed_cost', 'pets_allowed', 'pet_fee', 'pet_details'
        ]
    def update(self, instance, validated_data):
        instance.property = validated_data.get('property', instance.property)
        instance.checkin_time = validated_data.get('checkin_time', instance.checkin_time)
        instance.checkout_time = validated_data.get('checkout_time', instance.checkout_time)
        instance.children_allowed = validated_data.get('children_allowed', instance.children_allowed)
        instance.extra_beds_available = validated_data.get('extra_beds_available', instance.extra_beds_available)
        instance.extra_bed_cost = validated_data.get('extra_bed_cost', instance.extra_bed_cost)
        instance.pets_allowed = validated_data.get('pets_allowed', instance.pets_allowed)
        instance.pet_fee = validated_data.get('pet_fee', instance.pet_fee)
        instance.pet_details = validated_data.get('pet_details', instance.pet_details)
        instance.save()
        return instance

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

class RoomAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenities
        fields = [
            'id', 'air_conditioning', 'free_wifi', 'television', 'minibar', 'wardrobe', 'desk',
            'telephone', 'safe', 'soundproofing', 'ironing_facilities', 'extra_long_beds',
            'electric_blankets', 'garden_view', 'city_view', 'mountain_view', 'landmark_view',
            'pool_view', 'attached_bathroom', 'free_toiletries', 'shower', 'bathtub', 'bidet',
            'hairdryer', 'slippers', 'towels', 'toilet', 'balcony', 'patio', 'terrace',
            'private_entrance', 'kitchenette', 'heating'
        ]
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            'id', 'property', 'room_type', 'room_name', 'no_of_available_rooms', 'max_no_of_guests',
            'room_size', 'smoking_allowed', 'room_amenities'
        ]
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RoomBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBed
        fields = ['id', 'room_type', 'bed_type', 'quantity']
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'id', 'room_type', 'property', 'base_price_per_night', 'extra_guest_price',
            'breakfast_price', 'parking_price', 'is_seasonal', 'start_date', 'end_date',
            'discount_percentage', 'currency'
        ]
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RoomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = ['id', 'room_type', 'image']
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
class BulkRoomImagesSerializer(serializers.Serializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(),
        help_text="List of image files to upload"
    )

    def create(self, validated_data):
        room_type = validated_data['room_type']
        images = validated_data['images']
        room_images = [RoomImages(room_type=room_type, image=image) for image in images]
        return RoomImages.objects.bulk_create(room_images)
    

#########################offers###########################################
class WeeklyOfferSerializer(serializers.ModelSerializer):
    property_name = serializers.ReadOnlyField(source='property.property_name')

    class Meta:
        model = WeeklyOffer
        fields = ['id', 'property', 'property_name', 'discount_percentage', 'start_date', 'end_date', 'description']
        read_only_fields = ['id', 'property_name']

    def validate(self, data):
        # Ensure start_date is not greater than end_date
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be greater than end date.")
        return data

    def create(self, validated_data):
        return WeeklyOffer.objects.create(**validated_data)
    

######################PropertyFaqCreateSerializer#######################
class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFAQ
        fields = ['question_text']

class PropertyFAQCreateSerializer(serializers.ModelSerializer):
    replies = ReplyCreateSerializer(many=True, required=False)

    class Meta:
        model = PropertyFAQ
        fields = ['question_text', 'replies']

    def create(self, validated_data):
        replies_data = validated_data.pop('replies', [])
        faq = PropertyFAQ.objects.create(**validated_data)
        for reply_data in replies_data:
            PropertyFAQ.objects.create(
                property=faq.property,
                user=faq.user,
                parent=faq,
                question_text=reply_data['question_text']
            )

        return faq
