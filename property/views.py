
from rest_framework import generics
from django.db.models import Count,Q, Avg, Exists, OuterRef, Prefetch, F, Case, When, Value
from core.utils.pagination import CustomPageNumberPagination
from .models import City
from rest_framework.views import APIView  
from rest_framework.response import Response 
from rest_framework.generics import ListAPIView
from rest_framework import status  
from datetime import date 
from rooms.models import RoomType
from bookings.models import Booking
from .models import Property,PropertyCategory,CancellationPolicy,Policy,PropertyAmenities
from .serializers import CancellationPolicySerializer,PolicySerializer
from .serializers import TrendingDestinationSerializer,PropertySearchSerializer,PropertySerializer,PropertyCategorySerialzier,PropertyDetailsSerializer,PropertyAmenitiesSerializer,PropertyByCategorySerializer,MoredealspropertySerializer
from core.utils.response import PrepareResponse ,exception_response

# class PropertySearchView(APIView):
#     pagination_class = CustomPageNumberPagination  

#     def get(self, request):
#         try:
#             location = request.query_params.get('location', None)
#             check_in = request.query_params.get('check_in', None)
#             check_out = request.query_params.get('check_out', None)
#             adults = int(request.query_params.get('adults', 0) or 0)
#             children = int(request.query_params.get('children', 0) or 0)
#             rooms_requested = int(request.query_params.get('rooms', 1) or 1)
#             max_guests = adults + children
#             min_price = request.query_params.get('min_price', None)
#             max_price = request.query_params.get('max_price', None)
#             star_rating = request.query_params.get('star_rating', None)
#             property_type = request.query_params.get('property_type', None)
#             pets_allowed = request.query_params.get('pets_allowed', None)
#             free_cancellation = request.query_params.get('free_cancellation', None)
#             bed_type = request.query_params.get('bed_type', None)
#             guest_rating = request.query_params.get('guest_rating', None)

#             if not location:
#                 return PrepareResponse(
#                     success=False,
#                     message="Location is a required field.",
#                     errors={"location": "This field is required."}
#                 ).send(code=status.HTTP_400_BAD_REQUEST)

#             # ✅ Convert dates safely
#             if check_in and check_out:
#                 try:
#                     check_in = date.fromisoformat(check_in)
#                     check_out = date.fromisoformat(check_out)
#                     if check_in >= check_out:
#                         return PrepareResponse(
#                             success=False,
#                             message="Check-out must be after check-in.",
#                             errors={"check_out": "Must be after check-in."}
#                         ).send(code=status.HTTP_400_BAD_REQUEST)
#                 except ValueError:
#                     return PrepareResponse(
#                         success=False,
#                         message="Invalid date format. Use YYYY-MM-DD.",
#                         errors={"date_format": "Invalid format."}
#                     ).send(code=status.HTTP_400_BAD_REQUEST)

#             else:
#                 check_in, check_out = None, None

#             # ✅ Fastest way to check available rooms
#             available_rooms_subquery = RoomType.objects.filter(
#                 property=OuterRef('id'),
#                 no_of_available_rooms__gte=rooms_requested,
#                 max_no_of_guests__gte=max_guests
#             ).exclude(
#                 Exists(
#                     Booking.objects.filter(
#                         room=OuterRef('id'),  # ✅ Correct field reference
#                         check_in__lt=check_out,
#                         check_out__gt=check_in
#                     )
#                 )
#             ).values('id')[:1] if check_in and check_out else RoomType.objects.filter(
#                 property=OuterRef('id'),
#                 no_of_available_rooms__gte=rooms_requested,
#                 max_no_of_guests__gte=max_guests
#             ).values('id')[:1]
#             properties = Property.objects.filter(Q(city__city_name__icontains=location))\
#                 .select_related('city', 'country', 'currency', 'category')\
#                 .prefetch_related('images', 'amenities', 'room_type')\
#                 .defer('description', 'updated_at')\
#                 .annotate(
#                     avg_rating=Avg('reviews__rating'),
#                     review_count=Count('reviews'),
#                     has_available_rooms=Exists(available_rooms_subquery)
#                 ).filter(has_available_rooms=True)

#             # ✅ Apply only non-empty filters
#             if min_price is not None and max_price is not None:
#                 properties = properties.filter(single_unit_price__base_price_per_night__range=(min_price, max_price))

#             if star_rating:
#                 properties = properties.filter(star_rating_property__gte=int(star_rating))

#             if property_type:
#                 properties = properties.filter(category__category_name__icontains=property_type)

#             if pets_allowed is not None:
#                 properties = properties.filter(policies__pets_allowed=(pets_allowed.lower() == 'true'))

#             if free_cancellation is not None:
#                 properties = properties.filter(cancellation_policy__cancellation_fee_type='none')

#             if bed_type:
#                 properties = properties.filter(room_type__room_beds__bed_type__bed_type__iexact=bed_type.strip()).distinct()

#             if guest_rating:
#                 rating_threshold = {
#                     "9+": 9.0, "8+": 8.0, "7+": 7.0, "6+": 6.0
#                 }.get(guest_rating, None)
#                 if rating_threshold is not None:
#                     properties = properties.filter(avg_rating__gte=rating_threshold)

#             # ✅ **Apply Pagination**
#             paginator = self.pagination_class()
#             paginated_properties = paginator.paginate_queryset(properties, request)

#             serializer = PropertySearchSerializer(paginated_properties, many=True, context={
#                 'check_in': check_in,
#                 'check_out': check_out,
#                 'max_guests': max_guests,
#                 'rooms_requested': rooms_requested
#             })

#             paginated_data = paginator.get_paginated_response(serializer.data)

#             # ✅ **Return structured response**
#             return PrepareResponse(
#                 success=True,
#                 message="Properties fetched successfully.",
#                 data=paginated_data["results"],  # ✅ `results` inside `data`
#                 meta={  # ✅ Meta information
#                     "links": paginated_data["links"],
#                     "count": paginated_data["count"],
#                     "page_number": paginated_data["page_number"],
#                     "total_pages": paginated_data["total_pages"],
#                 }
#             ).send(code=status.HTTP_200_OK)

#         except Exception as e:
#             return exception_response(e)

class PropertySearchView(APIView):
    pagination_class = CustomPageNumberPagination  

    def get(self, request):
        try:
            location = request.query_params.get('location', None)
            check_in = request.query_params.get('check_in', None)
            check_out = request.query_params.get('check_out', None)
            adults = int(request.query_params.get('adults', 0) or 0)
            children = int(request.query_params.get('children', 0) or 0)
            rooms_requested = int(request.query_params.get('rooms', 1) or 1)
            max_guests = adults + children
            min_price = request.query_params.get('min_price', None)
            max_price = request.query_params.get('max_price', None)
            star_rating = request.query_params.get('star_rating', None)
            property_type = request.query_params.get('property_type', None)
            pets_allowed = request.query_params.get('pets_allowed', None)
            free_cancellation = request.query_params.get('free_cancellation', None)
            bed_type = request.query_params.get('bed_type', None)
            guest_rating = request.query_params.get('guest_rating', None)

            if not location:
                return PrepareResponse(
                    success=False,
                    message="Location is a required field.",
                    errors={"location": "This field is required."}
                ).send(code=status.HTTP_400_BAD_REQUEST)

            # ✅ Convert dates safely
            if check_in and check_out:
                try:
                    check_in = date.fromisoformat(check_in)
                    check_out = date.fromisoformat(check_out)
                    if check_in >= check_out:
                        return PrepareResponse(
                            success=False,
                            message="Check-out must be after check-in.",
                            errors={"check_out": "Must be after check-in."}
                        ).send(code=status.HTTP_400_BAD_REQUEST)
                except ValueError:
                    return PrepareResponse(
                        success=False,
                        message="Invalid date format. Use YYYY-MM-DD.",
                        errors={"date_format": "Invalid format."}
                    ).send(code=status.HTTP_400_BAD_REQUEST)

            else:
                check_in, check_out = None, None

            # ✅ Fastest way to check available rooms
            available_rooms_subquery = RoomType.objects.filter(
                property=OuterRef('id'),
                no_of_available_rooms__gte=rooms_requested,
                max_no_of_guests__gte=max_guests
            ).exclude(
                Exists(
                    Booking.objects.filter(
                        room=OuterRef('id'),  
                        check_in__lt=check_out,
                        check_out__gt=check_in
                    )
                )
            ).values('id')[:1] if check_in and check_out else RoomType.objects.filter(
                property=OuterRef('id'),
                no_of_available_rooms__gte=rooms_requested,
                max_no_of_guests__gte=max_guests
            ).values('id')[:1]

            # ✅ Include Single-Unit Properties (like Apartments) in the search
            properties = Property.objects.filter(
                Q(city__city_name__icontains=location)
            ).select_related('city', 'country', 'currency', 'category')\
                .prefetch_related('images', 'amenities', 'room_type')\
                .defer('description', 'updated_at')\
                .annotate(
                    avg_rating=Avg('reviews__rating'),
                    review_count=Count('reviews'),
                    has_available_rooms=Exists(available_rooms_subquery),
                    is_single_unit_available=Case(
                        When(is_single_unit=True, then=Value(True)),
                        default=F('has_available_rooms')
                    )
                ).filter(Q(is_single_unit_available=True)) 
            if min_price is not None and max_price is not None:
                properties = properties.filter(single_unit_price__base_price_per_night__range=(min_price, max_price))

            if star_rating:
                properties = properties.filter(star_rating_property__gte=int(star_rating))

            if property_type:
                properties = properties.filter(category__category_name__icontains=property_type)

            if pets_allowed is not None:
                properties = properties.filter(policies__pets_allowed=(pets_allowed.lower() == 'true'))

            if free_cancellation is not None:
                properties = properties.filter(cancellation_policy__cancellation_fee_type='none')

            if bed_type:
                properties = properties.filter(room_type__room_beds__bed_type__bed_type__iexact=bed_type.strip()).distinct()

            if guest_rating:
                rating_threshold = {
                    "9+": 9.0, "8+": 8.0, "7+": 7.0, "6+": 6.0
                }.get(guest_rating, None)
                if rating_threshold is not None:
                    properties = properties.filter(avg_rating__gte=rating_threshold)
            paginator = self.pagination_class()
            paginated_properties = paginator.paginate_queryset(properties, request)

            serializer = PropertySearchSerializer(paginated_properties, many=True, context={
                'check_in': check_in,
                'check_out': check_out,
                'max_guests': max_guests,
                'rooms_requested': rooms_requested
            })

            paginated_data = paginator.get_paginated_response(serializer.data)
            return PrepareResponse(
                success=True,
                message="Properties fetched successfully.",
                data=paginated_data["results"], 
                meta={
                    "links": paginated_data["links"],
                    "count": paginated_data["count"],
                    "page_number": paginated_data["page_number"],
                    "total_pages": paginated_data["total_pages"],
                }
            ).send(code=status.HTTP_200_OK)

        except Exception as e:
            return exception_response(e)
    
    
class PropertyListView(ListAPIView):
    queryset = Property.objects.select_related(
        'category', 'city'
    ).prefetch_related(
        'images', 'reviews'  
    ).annotate(
        avg_rating=Avg('reviews__rating'),  
        review_count=Count('reviews')
    )
    serializer_class = PropertySerializer
    
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

class TrendingDestinationsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        country_code = request.country_code 

        if not country_code:
            return PrepareResponse(
                success=False,
                message="Country code is required",
                errors={"country_code": "Missing country code in request"}
            ).send(400)
        cities = City.objects.annotate(
            property_count=Count('properties')
        ).filter(property_count__gt=0, country__country_code=country_code)  

        cities = cities.order_by('-property_count')[:5]  

        serializer = TrendingDestinationSerializer(cities, many=True)
        return PrepareResponse(
            success=True,
            message="Trending destinations retrieved successfully",
            data=serializer.data
        ).send(200)
    
class PropertyByPropertyTypeView(generics.ListAPIView):
    serializer_class = PropertyByCategorySerializer
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        property_type_id = self.kwargs.get('property_category_id')
        country_code = self.request.country_code
        if not country_code:
            return PropertyCategory.objects.none()
        queryset = PropertyCategory.objects.prefetch_related(
            Prefetch(
                'properties',
                queryset=Property.objects.select_related('category', 'city').prefetch_related('images', 'reviews').annotate(
                    avg_rating=Avg('reviews__rating'),
                    review_count=Count('reviews')
                ).order_by('-avg_rating', '-review_count')
            )
        ).filter(id=property_type_id, properties__country__country_code=country_code).distinct()

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()

        if not queryset:
            return PrepareResponse(
                success=False,
                message="Country code is required or no properties found for this category.",
                data=[]
            ).send(404)

        serializer = self.get_serializer(queryset)
        
        return PrepareResponse(
            success=True,
            message="Properties by property type retrieved successfully",
            data=serializer.data
        ).send(200)
    
class MoredealsPropertyListView(generics.ListAPIView):
    serializer_class=MoredealspropertySerializer

    def get(self,request,*args,**kwargs):
        properties=Property.objects.all()
        serializer=self.serializer_class(properties,many=True)
        return PrepareResponse(
            success=True,
            message="More deals properties fetched successfully",
            data=serializer.data
        ).send(200)

        
