from rest_framework import generics, permissions, status
from django.db.models import Avg
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from .models import PropertyReview, GuestReview
from property.models import Property
from .serializers import PropertyReviewSerializer, GuestReviewSerializer,GuestReviewAggregateSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination
from bookings.models import Booking

class PropertyReviewCreateView(generics.CreateAPIView):
    queryset = PropertyReview.objects.all()
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        property_slug = request.data.get('property_slug')

        # ✅ Validate and fetch property instance
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Invalid property slug.",
                errors={"property_slug": "Property with this slug does not exist."}
            ).send(status.HTTP_400_BAD_REQUEST)
        # booking_exists = Booking.objects.filter(
        #     user=request.user,
        #     property=property_instance,
        #     guest_status='checked_in'
        # ).exists()

        # if not booking_exists:
        #     raise PermissionDenied("You are not authorized to review this property. Please check in first.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['property_reviewed'] = property_instance 
        self.perform_create(serializer)

        return PrepareResponse(
            success=True,
            message="Property review created successfully",
            data=serializer.data
        ).send()

class PropertyReviewListView(generics.ListAPIView):
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')

        try:
            from property.models import Property
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PropertyReview.objects.none()
        return PropertyReview.objects.filter(
            property_reviewed=property_instance, parent__isnull=True
        ).prefetch_related('replies')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        review_count = queryset.count()

        # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response['review_count'] = review_count

            return PrepareResponse(
                success=True,
                message="Hotel review list retrieved successfully",
                data=paginated_response
            ).send(code=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Hotel review list retrieved successfully",
            data={
                'review_count': review_count,
                'results': serializer.data
            }
        ).send(code=status.HTTP_200_OK)

    

class GuestReviewListView(generics.ListAPIView):
    serializer_class = GuestReviewAggregateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return GuestReview.objects.none()  # We return aggregated data manually

    def list(self, request, *args, **kwargs):
        property_slug = self.kwargs.get('property_slug')

        # ✅ Fetch property instance
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Property not found.",
                errors={"property_slug": "Invalid property slug."}
            ).send(status.HTTP_400_BAD_REQUEST)

        # ✅ Get all reviews for the property
        reviews = GuestReview.objects.filter(property=property_instance)

        if not reviews.exists():
            return PrepareResponse(
                success=True,
                message="No reviews found for this property.",
                data={
                    "property_slug": property_slug,
                    "average_rating": None,
                    "category_averages": {}
                }
            ).send(status.HTTP_200_OK)

        # ✅ Compute all category averages in one query
        aggregation_results = reviews.aggregate(
            staff_avg=Avg("staff"),
            facilities_avg=Avg("facilities"),
            cleanliness_avg=Avg("cleanliness"),
            comfort_avg=Avg("comfort"),
            value_for_money_avg=Avg("value_for_money"),
            location_avg=Avg("location"),
            free_wifi_avg=Avg("free_wifi"),
        )

        category_averages = {
            "staff": round(aggregation_results["staff_avg"] or 0, 2),
            "facilities": round(aggregation_results["facilities_avg"] or 0, 2),
            "cleanliness": round(aggregation_results["cleanliness_avg"] or 0, 2),
            "comfort": round(aggregation_results["comfort_avg"] or 0, 2),
            "value_for_money": round(aggregation_results["value_for_money_avg"] or 0, 2),
            "location": round(aggregation_results["location_avg"] or 0, 2),
            "free_wifi": round(aggregation_results["free_wifi_avg"] or 0, 2),
        }

        # ✅ Compute overall average
        overall_average = sum(category_averages.values()) / len(category_averages)

        # ✅ Return response
        return PrepareResponse(
            success=True,
            message="Guest review averages retrieved successfully.",
            data={
                "property_slug": property_slug,
                "average_rating": round(overall_average, 2),
                "category_averages": category_averages
            }
        ).send(status.HTTP_200_OK)

    
class GuestReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        property_slug = request.data.get('property_slug')
        user = request.user
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Invalid property slug.",
                errors={"property_slug": "Property with this slug does not exist."}
            ).send(status.HTTP_400_BAD_REQUEST)
        # booking_exists = Booking.objects.filter(
        #     user=request.user,
        #     property=property_instance,
        #     guest_status='checked_in'
        # ).exists()

        # if not booking_exists:
        #     raise PermissionDenied("You are not authorized to review this property. Please check in first.")
        if GuestReview.objects.filter(user=user, property=property_instance).exists():
            return PrepareResponse(
                success=False,
                message="You have already reviewed this property.",
                errors={"property_slug": "A user can review a property only once."}
            ).send(status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['property'] = property_instance 
        serializer.validated_data['user'] = user 
        self.perform_create(serializer)

        return PrepareResponse(
            success=True,
            message="Guest review created successfully",
            data=serializer.data
        ).send()
    

##############################UserReviewList###################################
class UserPropertyReviewsListView(generics.ListAPIView):
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PropertyReview.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return PrepareResponse(
                success=True,
                message="User property reviews retrieved successfully",
                data=paginated_response
            ).send()

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="User property reviews retrieved successfully",
            data=serializer.data
        ).send()
    
class UserGuestReviewsListView(generics.ListAPIView):
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GuestReview.objects.filter(property__reviews__user=self.request.user).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return PrepareResponse(
                success=True,
                message="User guest reviews retrieved successfully",
                data=paginated_response
            ).send()

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="User guest reviews retrieved successfully",
            data=serializer.data
        ).send()
    

#######################Combined####################################
class CreateCombinedReviewView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        property_slug = request.data.get("property_slug")
        review_data = request.data.get("property_review")  # Property review details
        guest_review_data = request.data.get("guest_review")  # Guest review details

        # ✅ Validate Property Existence
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Property not found.",
                errors={"property_slug": "Invalid property slug."}
            ).send(status.HTTP_400_BAD_REQUEST)

        user = request.user
        response_data = {}

        with transaction.atomic():
            if review_data:
                # booking_exists = Booking.objects.filter(
                #     user=user,
                #     property=property_instance,
                #     guest_status="checked_in"
                # ).exists()

                # if not booking_exists:
                #     raise PermissionDenied("You are not authorized to review this property. Please check in first.")

                review_data["property_slug"] = property_slug
                review_serializer = PropertyReviewSerializer(data=review_data, context={"request": request})
                review_serializer.is_valid(raise_exception=True)
                review_serializer.validated_data["property_reviewed"] = property_instance
                review_serializer.save()

                response_data["property_review"] = review_serializer.data

            # ✅ Handle Guest Review (if provided)
            if guest_review_data:
                if GuestReview.objects.filter(user=user, property=property_instance).exists():
                    return PrepareResponse(
                        success=False,
                        message="You have already reviewed this property as a guest.",
                        errors={"property_slug": "A user can review a property only once."}
                    ).send(status.HTTP_400_BAD_REQUEST)

                guest_review_data["property_slug"] = property_slug
                guest_review_serializer = GuestReviewSerializer(data=guest_review_data, context={"request": request})
                guest_review_serializer.is_valid(raise_exception=True)
                guest_review_serializer.validated_data["property"] = property_instance
                guest_review_serializer.validated_data["user"] = user
                guest_review_serializer.save()

                response_data["guest_review"] = guest_review_serializer.data

        # ✅ Response
        return PrepareResponse(
            success=True,
            message="Reviews submitted successfully.",
            data=response_data
        ).send(status.HTTP_201_CREATED)

