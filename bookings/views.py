from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import ValidationError
from core.utils.response import PrepareResponse
from .models import Booking, RoomType, Property
from .serializers import BookingCreateSerializer
from core.utils.booking import calculate_booking_price 
from core.utils.cancellation import cancel_booking
from core.utils.moredealstoken import get_moredeals_token
import stripe
import requests
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class BookingCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BookingCreateSerializer(data=data, context={'request': request})

        if not serializer.is_valid():
            return PrepareResponse(
                success=False,
                data=serializer.errors,
                message="Booking creation failed"
            ).send(status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        total_price = calculate_booking_price(validated_data)

        try:
            with transaction.atomic():
                # Save the booking instance
                booking = serializer.save(user=request.user, total_price=total_price)

                # Process the payment
                payment_status, message = self.process_payment(
                    request=request,
                    payment_method=validated_data.get('payment_method'),
                    amount=total_price,
                    user=request.user,
                    booking=booking
                )

                # Update payment status in the booking instance
                booking.payment_status = payment_status.lower()
                booking.save()

                return PrepareResponse(
                    success=True,
                    message=message,
                    data={
                        "booking_id": booking.id,
                        "total_price": booking.total_price,
                        "payment_status": booking.payment_status,
                        "payment_method": booking.payment_method,
                    }
                ).send(status.HTTP_201_CREATED)
        except ValidationError as e:
            return PrepareResponse(
                success=False,
                message="Booking creation failed",
                errors={"payment_errors": str(e)}
            ).send(status.HTTP_400_BAD_REQUEST)

    def process_payment(self, request, payment_method, amount, user, booking):
        if payment_method == 'cod':
            booking.status = 'pending'
            booking.save()
            return 'Unpaid', "Booking placed with Cash on Arrival."
        elif payment_method == 'stripe':
            return self.process_stripe_payment(request, amount)
        elif payment_method == 'moredeals':
            return self.process_moredeals_payment(request, amount)
        else:
            raise ValidationError("Unsupported payment method.")

    def process_stripe_payment(self, request, amount):
        try:
            payment_method_id = request.data.get('payment_method_id')
            if not payment_method_id:
                raise ValidationError("Payment method ID not provided.")
            
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency="usd",
                payment_method=payment_method_id,
                confirmation_method="manual",
                confirm=True,
            )
            if payment_intent['status'] != 'succeeded':
                raise ValidationError(f"Payment failed with status: {payment_intent['status']}")
            return 'Paid', "Stripe payment successful."
        except stripe.error.CardError as e:
            raise ValidationError(str(e))

    def process_moredeals_payment(self, request, amount):
        """
        Process MoreDeals payment.
        """
        pin = request.data.get('pin')
        if not pin:
            raise ValidationError("PIN not provided for MoreDeals payment.")

        access_token = get_moredeals_token(request)
        response = requests.post(
            "https://moretrek.com/api/payments/payment-through-balance/",
            json={'amount': float(amount), 'pin': pin, 'platform': 'MoreLiving'},
            headers={'Authorization': f"Bearer {access_token}"}
        )

        if response.status_code == 200:
            return 'Paid', "MoreDeals payment successful."
        else:
            errors = response.json().get('errors', 'Unknown error')
            return 'Unpaid', f"MoreDeals payment failed: {errors}"
        
class BookingCancellationView(APIView):
    """
    View to handle booking cancellations.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)

            if booking.cancellation_status == 'canceled':
                return PrepareResponse(
                    success=False,
                    message="This booking has already been canceled.",
                ).send(status.HTTP_400_BAD_REQUEST)
            cancellation_data = cancel_booking(booking)

            return PrepareResponse(
                success=True,
                message=cancellation_data['message'],
                data={
                    "cancellation_fee": cancellation_data["cancellation_fee"],
                    "refundable_amount": cancellation_data["refundable_amount"],
                }
            ).send(status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Booking not found.",
                errors={"id": "Invalid booking ID."}
            ).send(status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return PrepareResponse(
                success=False,
                message=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
