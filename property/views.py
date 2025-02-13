
from rest_framework import generics
from django.db.models import Count
from .models import City
from rest_framework.views import APIView  
from rest_framework.response import Response 
from rest_framework import status  
from datetime import date  
from .models import Property,PropertyCategory,CancellationPolicy,Policy,PropertyAmenities
from .serializers import CancellationPolicySerializer,PolicySerializer

from .serializers import TrendingDestinationSerializer,PropertySearchSerializer,PropertySerializer,PropertyCategorySerialzier,PropertyDetailsSerializer,PropertyAmenitiesSerializer,PropertyByCategorySerializer
from core.utils.response import PrepareResponse
class PropertySearchView(APIView):
    def get(self, request):
        location = request.query_params.get('location', None)
        check_in = request.query_params.get('check_in', None)
        check_out = request.query_params.get('check_out', None)
        adults = int(request.query_params.get('adults', 0))
        children = int(request.query_params.get('children', 0))
        rooms_requested = int(request.query_params.get('rooms', 1)) 
        max_guests = adults + children
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        star_rating = request.query_params.get('star_rating', None)
        amenities = request.query_params.getlist('amenities', [])
        property_type = request.query_params.get('property_type', None)
        pets_allowed = request.query_params.get('pets_allowed', None)
        free_cancellation = request.query_params.get('free_cancellation', None)  

        if not location:
            return Response(
                {"error": "location is a required field."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional date validation
        if check_in and check_out:
            try:
                check_in = date.fromisoformat(check_in)
                check_out = date.fromisoformat(check_out)
                if check_in >= check_out:
                    return Response(
                        {"error": "check_out must be after check_in."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        properties = Property.objects.filter(
            city__city_name__icontains=location
        )
        if min_price and max_price:
            properties = properties.filter(single_unit_price__base_price_per_night__range=(min_price, max_price))

        if star_rating:
            properties = properties.filter(star_rating_property__gte=int(star_rating))

        if property_type:
            properties = properties.filter(category__category_name__icontains=property_type)

        if amenities:
            properties = properties.filter(amenities__amenity__name__in=amenities).distinct()

        if pets_allowed:
            properties = properties.filter(policies__pets_allowed=(pets_allowed.lower() == 'true'))

        if free_cancellation:
            properties = properties.filter(cancellation_policy__cancellation_fee_type='none')

        # Filter properties with available rooms if dates are provided
        if check_in and check_out:
            filtered_properties = []
            for property in properties:
                available_rooms = property.room_type.filter(
                    no_of_available_rooms__gte=rooms_requested,
                    max_no_of_guests__gte=max_guests
                ).exclude(
                    bookings__check_in__lt=check_out,
                    bookings__check_out__gt=check_in
                )
                if available_rooms.exists():
                    filtered_properties.append(property)
            properties = filtered_properties
        property_count = len(properties)

        serializer = PropertySearchSerializer(
            properties,
            many=True,
            context={
                'check_in': check_in,
                'check_out': check_out,
                'max_guests': max_guests,
                'rooms_requested': rooms_requested
            }
        )
        return Response({
            "property_count": property_count,
            "properties": serializer.data
        }, status=status.HTTP_200_OK)


class TrendingDestinationsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        cities = City.objects.annotate(
            property_count=Count('properties') 
        ).filter(property_count__gt=0).order_by('-property_count')[:6] 

        serializer = TrendingDestinationSerializer(cities, many=True)
        return PrepareResponse(
            success=True,
            message="Trending destinations retrieved successfully",
            data=serializer.data
        ).send(200)
    
class PropertyListView(APIView):

    def get(self, request):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PropertyCreateView(APIView):

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyDetailsView(generics.ListAPIView):
    serializer_class=PropertyDetailsSerializer

    def get_queryset(self):
        slug=self.kwargs.get('slug')
        queryset=Property.objects.filter(slug=slug)
        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Properties details fetched successfully",
            data=serializer.data
        ).send(200)
class PropertyCategoryListView(generics.ListAPIView):
    queryset = PropertyCategory.objects.all()
    serializer_class = PropertyCategorySerialzier

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Property categories retrieved successfully",
            data=serializer.data
        ).send(200)
    
class PropertyByPropertyTypeView(generics.ListAPIView):
    serializer_class = PropertyByCategorySerializer

    def get_queryset(self):
        property_type_id = self.kwargs.get('property_category_id')
        return PropertyCategory.objects.prefetch_related('properties').filter(id=property_type_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        if not queryset:
            return PrepareResponse(
                success=False,
                message="Category not found",
                data=[]
            ).send(404)

        serializer = self.get_serializer(queryset)
        return PrepareResponse(
            success=True,
            message="Properties by property type retrieved successfully",
            data=serializer.data
        ).send(200)
    
class PropertyCancellationPolicyView(APIView):

    def get(self, request, property_id, *args, **kwargs):
        try:
            cancellation_policy = CancellationPolicy.objects.get(property__id=property_id)
            serializer = CancellationPolicySerializer(cancellation_policy)

            return PrepareResponse(
                success=True,
                message="Cancellation policy retrieved successfully",
                data=serializer.data
            ).send(status.HTTP_200_OK)
        except CancellationPolicy.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Cancellation policy not found for the given property",
                errors={"property_id": "No cancellation policy exists for this property."}
            ).send(status.HTTP_404_NOT_FOUND)
        
class PolicyByPropertySlugView(generics.ListAPIView):
    serializer_class = PolicySerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        try:
            property_instance = Property.objects.get(slug=slug)
            return Policy.objects.filter(property=property_instance)
        except Property.DoesNotExist:
            return Policy.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return PrepareResponse(
                success=False,
                message="No policies found for the specified property.",
                data=[]
            ).send(status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Policies retrieved successfully for the specified property.",
            data=serializer.data
        ).send(status.HTTP_200_OK)
    
class PropertyAmenitiesListView(generics.ListAPIView):
    serializer_class = PropertyAmenitiesSerializer

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')

        # Fetch the property by slug
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PropertyAmenities.objects.none()

        # Return amenities related to the property
        return PropertyAmenities.objects.filter(property=property_instance)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return PrepareResponse(
                success=True,
                message="Property amenities retrieved successfully.",
                data=paginated_response
            ).send(code=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Property amenities retrieved successfully.",
            data=serializer.data
        ).send(code=status.HTTP_200_OK)

# class TrendingDestinationsView(generics.GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         country_code = request.country_code  # Get country code from middleware

#         # Filter cities that belong to the requested country
#         cities = City.objects.annotate(
#             property_count=Count('properties')
#         ).filter(property_count__gt=0)

#         if country_code:
#             cities = cities.filter(country__country_code=country_code)  # Apply country filter

#         cities = cities.order_by('-property_count')[:6]  # Limit to top 6

#         serializer = TrendingDestinationSerializer(cities, many=True)
#         return PrepareResponse(
#             success=True,
#             message="Trending destinations retrieved successfully",
#             data=serializer.data
#         ).send(200)
# class PropertyByPropertyTypeView(generics.ListAPIView):
#     serializer_class = PropertyByCategorySerializer

#     def get_queryset(self):
#         property_type_id = self.kwargs.get('property_category_id')
#         country_code = self.request.country_code  # Get country code from middleware

#         queryset = PropertyCategory.objects.prefetch_related('properties').filter(id=property_type_id)

#         if country_code:
#             queryset = queryset.filter(properties__country__country_code=country_code)

#         return queryset.distinct()

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset().first()
#         if not queryset:
#             return PrepareResponse(
#                 success=False,
#                 message="Category not found or no properties available in this country.",
#                 data=[]
#             ).send(404)

#         serializer = self.get_serializer(queryset)
#         return PrepareResponse(
#             success=True,
#             message="Properties by property type retrieved successfully",
#             data=serializer.data
#         ).send(200)
        
