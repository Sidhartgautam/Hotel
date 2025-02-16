from rest_framework import serializers
from .models import Booking
from datetime import date
from core.utils.booking import calculate_booking_price
from country.models import Country
from rest_framework import serializers
from datetime import date
from core.utils.booking import calculate_booking_price
from .models import Booking

class BookingCreateSerializer(serializers.ModelSerializer):
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
            'property', 'room', 'check_in', 'check_out', 'num_guests',
            'first_name', 'last_name','country_code', 'customer_email', 'payment_method', 'payment_method_id', 
            'pin', 'total_price'
        ]

    def validate(self, data):
        """
        Validate the booking data and payment details.
        """
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        payment_method = data.get('payment_method')
        property_obj = data.get('property')
        room = data.get('room')
        country_code = data.pop('country_code', None)  
        
        if country_code:
            try:
                country = Country.objects.get(country_code=country_code)
                data['country'] = country 
            except Country.DoesNotExist:
                raise serializers.ValidationError({"country_code": "Invalid country code."})

        ########validationforsingleunit
        if not room and not property_obj.is_single_unit:
            raise serializers.ValidationError({
                "room": "This property requires a room selection unless it is a single-unit property."
            })

        # Validate dates
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError({"check_in": "Check-in date must be earlier than check-out date."})

        if check_in and check_in < date.today():
            raise serializers.ValidationError({"check_in": "Check-in date cannot be in the past."})

        # Validate payment method-specific fields
        if payment_method == 'stripe' and not data.get('payment_method_id'):
            raise serializers.ValidationError({"payment_method_id": "Payment method ID is required for Stripe payments."})

        if payment_method == 'moredeals' and not data.get('pin'):
            raise serializers.ValidationError({"pin": "PIN is required for MoreDeals payment."})

        return data

    def create(self, validated_data):
        print("validated_data", validated_data)
        """
        Calculate the total price and create the booking.
        """
        validated_data.pop('pin', None)
        validated_data['total_price'] = calculate_booking_price(validated_data)
        return Booking.objects.create(**validated_data)
    
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

