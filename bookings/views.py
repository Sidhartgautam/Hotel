from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,generics
from django.db import transaction
from rest_framework.exceptions import ValidationError
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination
from .models import Booking, RoomType, Property
from .serializers import BookingCreateSerializer,BookingListSerializer
from core.utils.booking import calculate_booking_price 
from core.utils.cancellation import cancel_booking
from core.utils.moredealstoken import get_moredeals_token
from core.utils.booking_email import send_booking_confirmation_email
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
                booking = serializer.save(user=request.user, total_price=total_price, payment_status='pending')
                payment_status, message = self.process_payment(
                    request=request,
                    payment_method=validated_data.get('payment_method'),
                    payment_intent_id=validated_data.get('payment_method_id'),
                    amount=total_price,
                    booking=booking
                )

                if payment_status.lower() == 'paid':
                    booking.payment_status = 'paid'
                elif payment_status.lower() == 'unpaid' and validated_data.get('payment_method') == 'cod':
                    booking.payment_status = 'unpaid'
                else:
                    raise ValidationError({"payment_errors": message})

                booking.save()
                send_booking_confirmation_email(booking)

                return PrepareResponse(
                    success=True,
                    message="Booking created successfully.",
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
                message="Payment processing failed.",
                errors={"payment_errors": str(e)}
            ).send(status.HTTP_400_BAD_REQUEST)

    def process_payment(self, request, payment_method, payment_intent_id, amount, booking):
        """Handles different payment methods (Stripe, MoreDeals, COD)."""
        if payment_method == 'cod':
            return 'unpaid', "Booking placed with Cash on Arrival."

        elif payment_method == 'stripe':
            return self.confirm_stripe_payment(payment_intent_id)

        elif payment_method == 'moredeals':
            return self.process_moredeals_payment(request, amount, booking)

        else:
            raise ValidationError("Unsupported payment method.")

    def confirm_stripe_payment(self, payment_intent_id):
        """Confirms the Stripe PaymentIntent."""
        try:
            if not payment_intent_id:
                raise ValidationError("PaymentIntent ID not provided.")

            # Confirm the PaymentIntent
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent['status'] == 'succeeded':
                return 'paid', "Stripe payment successful."
            else:
                raise ValidationError(f"Payment failed with status: {payment_intent['status']}")

        except stripe.error.CardError as e:
            raise ValidationError(str(e))

    def process_moredeals_payment(self, request, amount, booking):
        pin = request.data.get('pin')
        if not pin:
            raise ValidationError("PIN not provided for MoreDeals payment.")

        property_obj = booking.property  

        if not property_obj:
            raise ValidationError("Property not found for this booking.")
        currency_code = property_obj.currency.currency_code
        recipient_username = property_obj.user.username

        access_token = get_moredeals_token(request)
        response = requests.post(
            "https://moretrek.com/api/payments/payment-through-balance/",
            json={'amount': float(amount), 'pin': pin, 'platform': 'moreliving', 'currency_code': currency_code, 'recipient': recipient_username},
            headers={'Authorization': f"{access_token}"}
        )
        if response.status_code == 200 and response.json().get('success', False):
            return 'paid', "MoreDeals payment successful."
        else:
            errors = response.json().get('errors', 'Unknown error')
            raise ValidationError(f"MoreDeals payment failed: {errors}")
        
class BookingCancellationView(APIView):
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
        
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        booking_count = queryset.count()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            # Ensure paginated_response is a Response object
            paginated_response_data = paginated_response
            paginated_response_data['booking_count'] = booking_count

            return PrepareResponse(
                success=True,
                message="User bookings retrieved successfully",
                data=paginated_response_data  # Use the modified data
            ).send(code=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="User bookings retrieved successfully",
            data={
                'booking_count': booking_count,
                'results': serializer.data
            }
        ).send(code=status.HTTP_200_OK)
