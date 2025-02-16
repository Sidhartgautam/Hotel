import json
import stripe
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Set Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Create a payment intent for Stripe transactions.
        """
        try:
            data = json.loads(request.body)
            amount = data.get('amount', 0)
            currency = data.get('currency', 'usd')

            if amount <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100), 
                currency=currency,
                payment_method_types=["card"],
            )

            return Response({
                "success": True,
                "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id
            }, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
