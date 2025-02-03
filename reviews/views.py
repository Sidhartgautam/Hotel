from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import PropertyReview, GuestReview
from .serializers import PropertyReviewSerializer, GuestReviewSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination
from bookings.models import Booking

class PropertyReviewCreateView(generics.CreateAPIView):
    queryset = PropertyReview.objects.all()
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if the user has a valid booking and has checked in
        property_id = request.data.get('property')
        booking_exists = Booking.objects.filter(
            user=request.user,
            property_id=property_id,
            status='checked_in'
        ).exists()

        if not booking_exists:
            raise PermissionDenied("You are not authorized to review this property. Please check in first.")

        # Proceed to create the review
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.AllowAny]  # Use `IsAuthenticated` if necessary
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')

        # Filter by the property with the given slug
        try:
            from property.models import Property
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return GuestReview.objects.none()

        return GuestReview.objects.filter(property=property_instance)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return PrepareResponse(
                success=True,
                message="Guest review list retrieved successfully",
                data=paginated_response
            ).send(code=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Guest review list retrieved successfully",
            data=serializer.data
        ).send(code=status.HTTP_200_OK)

    
class GuestReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        property_id = request.data.get('property')
        booking_exists = Booking.objects.filter(
            user=request.user,
            property_id=property_id,
            status='checked_in'
        ).exists()

        if not booking_exists:
            raise PermissionDenied("You are not authorized to review this property. Please check in first.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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

