# currency/views.py
from rest_framework import generics
from .models import Currency
from .serializers import CurrencySerializer
from core.utils.response import PrepareResponse

class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = []  # No authentication required

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Currency list retrieved successfully",
            data=serializer.data
        )
        return response.send()
