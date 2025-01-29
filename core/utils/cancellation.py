from datetime import date, timedelta
from decimal import Decimal

def cancel_booking(booking):
    property_policy = booking.property.cancellation_policy.first()  # Assuming one policy per property

    if not property_policy:
        raise ValueError("No cancellation policy is defined for this property.")
    if not property_policy.cancellations_allowed:
        raise ValueError("Cancellations are not allowed for this property.")
    days_before_check_in = (booking.check_in - date.today()).days
    if days_before_check_in < property_policy.cancellation_deadline_days:
        raise ValueError(f"Cancellations are only allowed up to {property_policy.cancellation_deadline_days} days before check-in.")
    if property_policy.cancellation_fee_type == 'percentage':
        cancellation_fee = (property_policy.cancellation_fee_amount / Decimal(100)) * booking.total_price
    elif property_policy.cancellation_fee_type == 'fixed':
        cancellation_fee = property_policy.cancellation_fee_amount
    else:
        cancellation_fee = Decimal(0)
    if not property_policy.refundable:
        refundable_amount = Decimal(0)
    else:
        refundable_amount = booking.total_price - cancellation_fee
    booking.cancellation_status = 'canceled'
    booking.cancellation_date = date.today()
    booking.save()

    return {
        "cancellation_fee": round(cancellation_fee, 2),
        "refundable_amount": round(refundable_amount, 2),
        "message": "Booking canceled successfully."
    }
