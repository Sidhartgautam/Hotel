from datetime import timedelta, date
from rooms.models import Price
from offers.models import WeeklyOffer
from property.models import SingleUnitPrice

# def calculate_booking_price(validated_data):
#     """
#     Calculate the total price for a booking. Handles both single-unit and multi-room properties.
#     """
#     property_obj = validated_data.get('property')
#     room = validated_data.get('room')
#     check_in = validated_data.get('check_in')
#     check_out = validated_data.get('check_out')
#     num_guests = validated_data.get('num_guests', 1)
#     nights = (check_out - check_in).days
#     if nights <= 0:
#         raise ValueError("Check-out date must be later than check-in date.")

#     # Handle single-unit property pricing
#     if property_obj.is_single_unit:
#         if not hasattr(property_obj, 'single_unit_price'):
#             raise ValueError("Single-unit price is not defined for this property.")

#         # Get the effective price for the single unit
#         base_price = property_obj.single_unit_price.get_effective_price() * nights
#     else:
#         # Handle multi-room property pricing
#         if not room:
#             raise ValueError("Room must be provided for multi-room properties.")

#         # Fetch the price object for the room
#         try:
#             price = Price.objects.get(room_type=room)
#         except Price.DoesNotExist:
#             raise ValueError("Price for the selected room type is not defined.")

#         # Calculate the base price for the stay
#         base_price = price.base_price_per_night * nights

#         # Calculate extra charges
#         extra_guest_price = 0
#         if num_guests > room.max_no_of_guests:
#             extra_guest_price = (num_guests - room.max_no_of_guests) * price.extra_guest_price * nights

#         # Optional extra charges
#         breakfast_price = price.breakfast_price * nights if validated_data.get('include_breakfast', False) else 0
#         parking_price = price.parking_price * nights if validated_data.get('include_parking', False) else 0

#         # Add extra charges to the base price
#         base_price += extra_guest_price + breakfast_price + parking_price


#     # Apply dynamic offers (if available)
#     total_price = apply_offer(property_obj, check_in, check_out, base_price)

#     return round(total_price, 2)


# def apply_offer(property_obj, check_in, check_out, base_price):
#     """
#     Apply seasonal and weekly offers to the base price and return the final price.
#     """
#     best_discount = 0

#     # Apply seasonal pricing if applicable
#     seasonal_price = Price.objects.filter(
#         property=property_obj,
#         is_seasonal=True,
#         start_date__lte=check_out,
#         end_date__gte=check_in
#     ).first()
#     if seasonal_price:
#         seasonal_discount = (seasonal_price.discount_percentage / 100) * base_price
#         best_discount = max(best_discount, seasonal_discount)

#     # Apply weekly offers if applicable
#     weekly_offer = WeeklyOffer.objects.filter(
#         property=property_obj,
#         start_date__lte=check_out,
#         end_date__gte=check_in
#     ).first()
#     if weekly_offer:
#         weekly_discount = (weekly_offer.discount_percentage / 100) * base_price
#         best_discount = max(best_discount, weekly_discount)

#     # Apply the best discount
#     return base_price - best_discount


def calculate_booking_price(validated_data):
    property_obj = validated_data.get('property')
    room = validated_data.get('room')
    check_in = validated_data.get('check_in')
    check_out = validated_data.get('check_out')
    num_guests = validated_data.get('num_guests', 1)
    num_rooms = validated_data.get('num_rooms', 1)  # Default to 1 if not provided

    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Check-out date must be later than check-in date.")

    # Handle single-unit property pricing
    if property_obj.is_single_unit:
        if not hasattr(property_obj, 'single_unit_price'):
            raise ValueError("Single-unit price is not defined for this property.")

        # Get the effective price for the single unit
        base_price = property_obj.single_unit_price.get_effective_price() * nights
    else:
        # Handle multi-room property pricing
        if not room:
            raise ValueError("Room must be provided for multi-room properties.")

        # Fetch the price object for the room
        try:
            price = Price.objects.get(room_type=room)
        except Price.DoesNotExist:
            raise ValueError("Price for the selected room type is not defined.")

        # Calculate the base price for the stay
        base_price_per_room = price.base_price_per_night * nights

        # Calculate extra charges
        extra_guest_price = 0
        if num_guests > room.max_no_of_guests:
            extra_guest_price = (num_guests - room.max_no_of_guests) * price.extra_guest_price * nights

        # Optional extra charges
        breakfast_price = price.breakfast_price * nights if validated_data.get('include_breakfast', False) else 0
        parking_price = price.parking_price * nights if validated_data.get('include_parking', False) else 0

        # Add extra charges per room
        base_price_per_room += extra_guest_price + breakfast_price + parking_price

        # Multiply by number of rooms
        base_price = base_price_per_room * num_rooms

    # Apply dynamic offers (if available)
    total_price = apply_offer(property_obj, check_in, check_out, base_price)

    return round(total_price, 2)


def apply_offer(property_obj, check_in, check_out, base_price):
    """
    Apply seasonal and weekly offers to the base price and return the final price.
    """
    best_discount = 0

    # Apply seasonal pricing if applicable
    seasonal_price = Price.objects.filter(
        property=property_obj,
        is_seasonal=True,
        start_date__lte=check_out,
        end_date__gte=check_in
    ).first()
    if seasonal_price:
        seasonal_discount = (seasonal_price.discount_percentage / 100) * base_price
        best_discount = max(best_discount, seasonal_discount)

    # Apply weekly offers if applicable
    weekly_offer = WeeklyOffer.objects.filter(
        property=property_obj,
        start_date__lte=check_out,
        end_date__gte=check_in
    ).first()
    if weekly_offer:
        weekly_discount = (weekly_offer.discount_percentage / 100) * base_price
        best_discount = max(best_discount, weekly_discount)

    # Apply the best discount
    return base_price - best_discount
