from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_booking_confirmation_email(booking):
    """
    Sends booking confirmation emails to both the user and the hotel.
    """
    user_email = booking.customer_email
    hotel_email = booking.property.user.email  
    subject = f"Booking Confirmation - {booking.property.property_name}"

    # Context data for email templates
    context = {
        "first_name": booking.first_name,
        "last_name": booking.last_name,
        "property_name": booking.property.property_name,
        "room_name": booking.room.room_name if booking.room else 'Entire Property',
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "num_guests": booking.num_guests,
        "total_price": f"{booking.total_price} {booking.property.currency.currency_code}",
        "payment_method": booking.payment_method.upper(),
        "payment_status": booking.payment_status.upper(),
        "hotel_owner_name": booking.property.user.first_name
    }

    # Render email templates
    user_message = render_to_string('email_templates/booking_confirmation_user.txt', context)
    hotel_message = render_to_string('email_templates/booking_confirmation_hotel.txt', context)

    # Send mail to the booked user
    send_mail(
        subject=subject,
        message=user_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )

    # Send mail to the hotel owner
    send_mail(
        subject=f"New Booking Alert - {booking.property.property_name}",
        message=hotel_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[hotel_email],
        fail_silently=False,
    )
