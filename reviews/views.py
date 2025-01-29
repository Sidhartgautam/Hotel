from rest_framework import generics, permissions, status
from .models import PropertyReview, GuestReview
from .serializers import PropertyReviewSerializer, GuestReviewSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination

class PropertyReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = PrepareResponse(
            success=True,
            message="Review created successfully",
            data=serializer.data
        ).send(200)

class HotelReviewListView(generics.ListAPIView):
    queryset = PropertyReview.objects.all()
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel review list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    

class GuestReviewListView(generics.ListAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Guest review list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    
class GuestReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = PrepareResponse(
            success=True,
            message="Guest review created successfully",
            data=serializer.data
        )
        return response.send()

