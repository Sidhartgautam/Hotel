from rest_framework import generics
from .models import Country,City
from django.db.models import Count
from .serializers import CountrySerializer, CitySerializer,PopularCitySerializer
from core.utils.response import PrepareResponse
from rest_framework import permissions

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    # permission_classes = [permissions.IsAdminUser] 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Country list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
    
# class CityListView(generics.ListAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         response = PrepareResponse(
#             success=True,
#             message="City list retrieved successfully",
#             data=serializer.data
#         )
#         return response.send(200)
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        country_code = self.request.country_code 

        if not country_code:
            return City.objects.none()  

        return City.objects.filter(country__country_code=country_code) 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():  
            return PrepareResponse(
                success=True,
                message="No cities found",
                data=None  
            ).send(200)

        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="City list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
    
class PopularCityView(generics.GenericAPIView):
    serializer_class = PopularCitySerializer

    def get_queryset(self):
        return City.objects.annotate(hotel_count=Count('hotels')).order_by('-hotel_count')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Popular cities retrieved successfully",
            data=serializer.data
        ).send(200)
