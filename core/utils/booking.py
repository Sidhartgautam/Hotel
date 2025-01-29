from datetime import timedelta
from rooms.models import Price
from offers.models import WeeklyOffer


# def calculate_booking_price(validated_data):
#     room = validated_data.get('room')
#     check_in = validated_data.get('check_in')
#     check_out = validated_data.get('check_out')
#     num_guests = validated_data.get('num_guests', 1)

#     # Fetch the price object for the room
#     try:
#         price = Price.objects.get(room_type=room)
#     except Price.DoesNotExist:
#         raise ValueError("Price for the selected room type is not defined.")

#     # Calculate the number of nights
#     nights = (check_out - check_in).days
#     if nights <= 0:
#         raise ValueError("Check-out date must be later than check-in date.")

#     # Calculate the base price for the stay
#     base_price = price.base_price_per_night * nights

#     # Calculate extra charges for additional guests
#     extra_guest_price = 0
#     if num_guests > 1:  # Assuming base capacity is 1 guest
#         extra_guest_price = (num_guests - 1) * price.extra_guest_price * nights

#     # Calculate additional charges (e.g., breakfast, parking)
#     breakfast_price = price.breakfast_price * nights if validated_data.get('include_breakfast', False) else 0
#     parking_price = price.parking_price * nights if validated_data.get('include_parking', False) else 0

#     # Apply any discounts
#     discount = 0
#     if price.discount_percentage > 0:
#         discount = (base_price + extra_guest_price + breakfast_price + parking_price) * (price.discount_percentage / 100)

#     # Total price calculation
#     total_price = base_price + extra_guest_price + breakfast_price + parking_price - discount

#     return round(total_price, 2)
from datetime import date

def calculate_booking_price(validated_data):
    room = validated_data.get('room')
    property_obj = validated_data.get('property')
    check_in = validated_data.get('check_in')
    check_out = validated_data.get('check_out')
    num_guests = validated_data.get('num_guests', 1)

    # Fetch the price object for the room
    try:
        price = Price.objects.get(room_type=room)
    except Price.DoesNotExist:
        raise ValueError("Price for the selected room type is not defined.")

    # Calculate the number of nights
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Check-out date must be later than check-in date.")

    # Calculate the base price for the stay
    base_price = price.base_price_per_night * nights

    # Apply dynamic offers if available
    base_price = apply_offer(property_obj, check_in, check_out, base_price)

    # Calculate extra charges for additional guests
    extra_guest_price = 0
    if num_guests > 1:  # Assuming base capacity is 1 guest
        extra_guest_price = (num_guests - 1) * price.extra_guest_price * nights

    # Calculate additional charges (e.g., breakfast, parking)
    breakfast_price = price.breakfast_price * nights if validated_data.get('include_breakfast', False) else 0
    parking_price = price.parking_price * nights if validated_data.get('include_parking', False) else 0

    # Apply any discounts
    discount = 0
    if price.discount_percentage > 0:
        discount = (base_price + extra_guest_price + breakfast_price + parking_price) * (price.discount_percentage / 100)

    # Total price calculation
    total_price = base_price + extra_guest_price + breakfast_price + parking_price - discount

    return round(total_price, 2)


def apply_offer(property_obj, check_in, check_out, base_price):
    best_discount = 0
    seasonal_price = Price.objects.filter(
        property=property_obj,
        is_seasonal=True,
        start_date__lte=check_out,
        end_date__gte=check_in
    ).first()
    if seasonal_price:
        seasonal_discount = (seasonal_price.discount_percentage / 100) * base_price
        best_discount = max(best_discount, seasonal_discount)
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
