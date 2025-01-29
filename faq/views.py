from rest_framework import generics, permissions
from .models import PropertyFAQ, MoreLivingFAQ
from .serializers import PropertyFAQSerializer, WebsiteFAQSerializer
from property.models import Property
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination


# Hotel FAQ Views
class PropertyFAQCreateView(generics.GenericAPIView):
    serializer_class = PropertyFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id')
        try:
            property = Property.objects.get(id=hotel_id)
        except Property.DoesNotExist:
            return PrepareResponse(success=False, message="Hotel not found").send(404)

        parent_id = request.data.get('parent')
        if parent_id:
            try:
                parent_faq = PropertyFAQ.objects.get(id=parent_id, property=property)

                if parent_faq.parent is not None:
                    return PrepareResponse(success=False, message="Replies cannot have further replies").send(400)
                if request.user != property.user:
                    return PrepareResponse(success=False, message="Only property owner can add replies").send(403)
            except PropertyFAQ.DoesNotExist:
                return PrepareResponse(success=False, message="Parent FAQ not found").send(404)
        else:
            parent_faq = None

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property, user=request.user, parent=parent_faq)
            return PrepareResponse(success=True, data=serializer.data, message="Property FAQ added").send(201)
        
        return PrepareResponse(success=False, data=serializer.errors, message="Failed to add FAQ").send(400)


class PropertyFAQListView(generics.ListAPIView):
    serializer_class = PropertyFAQSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        property_id = self.kwargs.get('hotel_id')
        return PropertyFAQ.objects.filter(property_id=property_id, parent__isnull=True).order_by('-created_at')


# Website FAQ Views
class WebsiteFAQCreateView(generics.CreateAPIView):
    queryset = MoreLivingFAQ.objects.all()
    serializer_class = WebsiteFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent_faq = MoreLivingFAQ.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, parent=parent_faq)


class WebsiteFAQListView(generics.ListAPIView):
    serializer_class = WebsiteFAQSerializer
    queryset = MoreLivingFAQ.objects.filter(parent__isnull=True).order_by('-created_at')
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.AllowAny]
