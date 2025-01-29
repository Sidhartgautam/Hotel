from rest_framework import serializers
from .models import Booking
from datetime import date
from core.utils.booking import calculate_booking_price

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

    class Meta:
        model = Booking
        fields = [
            'property', 'room', 'check_in', 'check_out', 'num_guests',
            'customer_name', 'customer_email', 'payment_method', 'payment_method_id', 
            'pin', 'total_price'
        ]

    def validate(self, data):
        """
        Validate the booking data and payment details.
        """
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        payment_method = data.get('payment_method')

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
        """
        Calculate the total price and create the booking.
        """
        validated_data['total_price'] = calculate_booking_price(validated_data)
        return Booking.objects.create(**validated_data)

