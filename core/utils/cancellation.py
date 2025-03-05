from datetime import date, timedelta
from decimal import Decimal
from rooms.models import RoomAvailability

def cancel_booking(booking):
    property_policy = booking.property.cancellation_policy.first()  
    if not property_policy:
        raise ValueError("No cancellation policy is defined for this property.")
    
    if not property_policy.cancellations_allowed:
        raise ValueError("Cancellations are not allowed for this property.")
    
    days_before_check_in = (booking.check_in - date.today()).days
    cancellation_deadline_days = property_policy.cancellation_deadline_days if property_policy.cancellation_deadline_days is not None else 0

    if days_before_check_in < cancellation_deadline_days:
        raise ValueError(f"Cancellations are only allowed up to {cancellation_deadline_days} days before check-in.")
    if property_policy.cancellation_fee_type == 'percentage':
        cancellation_fee = (property_policy.cancellation_fee_amount / Decimal(100)) * booking.total_price
    elif property_policy.cancellation_fee_type == 'fixed':
        cancellation_fee = property_policy.cancellation_fee_amount
    else:
        cancellation_fee = Decimal(0) 
    refundable_amount = Decimal(0)

    if booking.payment_method in ["stripe", "moredeals"] and property_policy.refundable:
        refundable_amount = booking.total_price - cancellation_fee 
    booking.cancellation_status = 'canceled'
    booking.cancellation_date = date.today()
    booking.save()
    if booking.room:
        current_date = booking.check_in
        while current_date < booking.check_out:
            room_availability, created = RoomAvailability.objects.get_or_create(
                room_type=booking.room, date=current_date
            )
            room_availability.available_rooms += 1  
            room_availability.save()
            current_date += timedelta(days=1)

    return {
        "cancellation_fee": round(cancellation_fee, 2),
        "refundable_amount": round(refundable_amount, 2),
        "message": "Booking canceled successfully, and room availability restored."
    }
