from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import WeeklyOffer
from .serializers import WeeklyOfferSerializer,AllOfferSerializer
from core.utils.response import PrepareResponse

class WeeklyOffersView(APIView):
    def get(self, request):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        country_code = request.country_code 
        if not country_code:
            return Response({
                "success": False,
                "message": "Country code is required.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_date = date.fromisoformat(from_date) if from_date else None
            to_date = date.fromisoformat(to_date) if to_date else None
        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid date format. Use 'YYYY-MM-DD'.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
        if from_date and to_date and from_date > to_date:
            return Response({
                "success": False,
                "message": "'from' date must be earlier than or equal to 'to' date.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
        weekly_offers = WeeklyOffer.objects.filter(property__country__country_code=country_code)
        if from_date and to_date:
            weekly_offers = weekly_offers.filter(
                start_date__lte=to_date, 
                end_date__gte=from_date  
            )
        serializer = WeeklyOfferSerializer(weekly_offers, many=True)

        return Response({
            "success": True,
            "message": "Weekly offers retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class AllOffersView(APIView):
    serializer_class = AllOfferSerializer

    def get(self, request):
        weekly_offers = WeeklyOffer.objects.all()
        serializer = self.serializer_class(weekly_offers, many=True)
        return PrepareResponse(
            success=True,
            message="Weekly offers retrieved successfully",
            data=serializer.data
        ).send(status.HTTP_200_OK)

