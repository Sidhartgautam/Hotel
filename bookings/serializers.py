from rest_framework import serializers
from .models import Booking
from property.models import Property
from datetime import date
from core.utils.booking import calculate_booking_price
from country.models import Country
from rest_framework import serializers
from datetime import date
from core.utils.booking import calculate_booking_price
from .models import Booking
from rooms.models import RoomAvailability
from django.db import transaction
from datetime import timedelta

# class BookingCreateSerializer(serializers.ModelSerializer):
#     property_slug = serializers.CharField(
#         required=True, help_text="Slug of the property instead of property ID."
#     )
#     payment_method = serializers.ChoiceField(
#         choices=['cod', 'stripe', 'moredeals'],
#         required=True,
#         help_text="Payment method (cod, stripe, moredeals)"
#     )
#     payment_method_id = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         help_text="Stripe payment method ID (required for Stripe payment)."
#     )
#     pin = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         help_text="PIN for MoreDeals payment."
#     )
#     total_price = serializers.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         read_only=True, 
#         help_text="Total price for the booking, including offers and discounts."
#     )
#     country_code = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         help_text="Country code instead of country ID."
#     )

#     class Meta:
#         model = Booking
#         fields = [
#             'property_slug', 'room', 'check_in', 'check_out', 'num_guests',
#             'first_name', 'last_name','country_code', 'customer_email', 'payment_method', 'payment_method_id', 
#             'pin', 'total_price'
#         ]

#     def validate(self, data):
#         check_in = data.get('check_in')
#         check_out = data.get('check_out')
#         payment_method = data.get('payment_method')
#         property_obj = data.get('property')
#         room = data.get('room')
#         country_code = data.pop('country_code', None) 
#         property_slug = data.pop('property_slug', None)

#         try:
#             property_obj = Property.objects.get(slug=property_slug)
#             data['property'] = property_obj
#         except Property.DoesNotExist:
#             raise serializers.ValidationError({"property_slug": "Invalid property slug."}) 
        
#         if country_code:
#             try:
#                 country = Country.objects.get(country_code=country_code)
#                 data['country'] = country 
#             except Country.DoesNotExist:
#                 raise serializers.ValidationError({"country_code": "Invalid country code."})

#         ########validationforsingleunit
#         if not room and not property_obj.is_single_unit:
#             raise serializers.ValidationError({
#                 "room": "This property requires a room selection unless it is a single-unit property."
#             })

#         # Validate dates
#         if check_in and check_out and check_in >= check_out:
#             raise serializers.ValidationError({"check_in": "Check-in date must be earlier than check-out date."})

#         if check_in and check_in < date.today():
#             raise serializers.ValidationError({"check_in": "Check-in date cannot be in the past."})

#         # Validate payment method-specific fields
#         if payment_method == 'stripe' and not data.get('payment_method_id'):
#             raise serializers.ValidationError({"payment_method_id": "Payment method ID is required for Stripe payments."})

#         if payment_method == 'moredeals' and not data.get('pin'):
#             raise serializers.ValidationError({"pin": "PIN is required for MoreDeals payment."})

#         return data

#     def create(self, validated_data):
#         print("validated_data",validated_data)
#         validated_data.pop('pin', None)
#         validated_data['total_price'] = calculate_booking_price(validated_data)
#         return Booking.objects.create(**validated_data)

class BookingCreateSerializer(serializers.ModelSerializer):
    property_slug = serializers.CharField(
        required=True, help_text="Slug of the property instead of property ID."
    )
    payment_method = serializers.ChoiceField(
        choices=['cod', 'stripe', 'moredeals'],
        required=True,
        help_text="Payment method (cod, stripe, moredeals)"
    )
    payment_method_id = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Stripe payment method ID (required for Stripe payment)."
    )
    pin = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="PIN for MoreDeals payment."
    )
    total_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True, 
        help_text="Total price for the booking, including offers and discounts."
    )
    country_code = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Country code instead of country ID."
    )

    class Meta:
        model = Booking
        fields = [
            'property_slug', 'room', 'check_in', 'check_out', 'num_guests',
            'first_name', 'last_name', 'country_code', 'customer_email', 
            'payment_method', 'payment_method_id', 'pin', 'total_price'
        ]

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        payment_method = data.get('payment_method')
        room = data.get('room')
        property_slug = data.pop('property_slug', None)
        country_code = data.pop('country_code', None) 

        # ✅ Ensure Property Exists
        try:
            property_obj = Property.objects.get(slug=property_slug)
            data['property'] = property_obj
        except Property.DoesNotExist:
            raise serializers.ValidationError({"property_slug": "Invalid property slug."}) 
        
        # ✅ Ensure Country Exists (if provided)
        if country_code:
            try:
                country = Country.objects.get(country_code=country_code)
                data['country'] = country 
            except Country.DoesNotExist:
                raise serializers.ValidationError({"country_code": "Invalid country code."})

        # ✅ Validate Dates
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError({"check_in": "Check-in date must be earlier than check-out date."})
            if check_in < date.today():
                raise serializers.ValidationError({"check_in": "Check-in date cannot be in the past."})

        # ✅ Validate Payment Method Fields
        if payment_method == 'stripe' and not data.get('payment_method_id'):
            raise serializers.ValidationError({"payment_method_id": "Payment method ID is required for Stripe payments."})

        if payment_method == 'moredeals' and not data.get('pin'):
            raise serializers.ValidationError({"pin": "PIN is required for MoreDeals payment."})

        # ✅ Handle Single-Unit Property Bookings
        if property_obj.is_single_unit:
            data['room'] = None  # Single-unit properties don't have rooms, so we set this to None
        else:
            # ✅ Validate Room Availability for Multi-Room Properties
            if not room:
                raise serializers.ValidationError({
                    "room": "This property requires a room selection unless it is a single-unit property."
                })

            unavailable_dates = []
            for single_date in (check_in + timedelta(n) for n in range((check_out - check_in).days)):
                room_availability = RoomAvailability.objects.filter(
                    room_type=room,
                    date=single_date,
                    available_rooms__gt=0
                ).first()

                if not room_availability:
                    unavailable_dates.append(single_date)

            if unavailable_dates:
                raise serializers.ValidationError(
                    f"No available rooms for {room.room_name} on {', '.join(map(str, unavailable_dates))}"
                )

        return data

    def create(self, validated_data):
        validated_data.pop('pin', None)
        total_price = calculate_booking_price(validated_data) 
        validated_data['total_price'] = total_price
        room = validated_data.get('room')
        check_in = validated_data.get('check_in')
        check_out = validated_data.get('check_out')

        with transaction.atomic():
            # ✅ Create Booking
            booking = Booking.objects.create(**validated_data)
            if room:
                for single_date in (check_in + timedelta(n) for n in range((check_out - check_in).days)):
                    room_availability, created = RoomAvailability.objects.get_or_create(
                        room_type=room, date=single_date
                    )

                    if room_availability.available_rooms > 0:
                        room_availability.available_rooms -= 1  
                        room_availability.save()
                    else:
                        raise serializers.ValidationError(
                            f"No available rooms for {room.room_name} on {single_date}"
                        )

        return booking

    
class BookingListSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.property_name', read_only=True)
    room_name = serializers.CharField(source='room.room_name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'property_name', 'room_name', 'check_in', 'check_out', 'num_guests',
            'first_name', 'last_name','country', 'customer_email', 'total_price', 'payment_status',
            'cancellation_status', 'booking_date'
        ]
        read_only_fields = fields

