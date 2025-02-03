from rest_framework import generics, permissions,status
from .models import PropertyFAQ, MoreLivingFAQ
from .serializers import PropertyFAQSerializer,PropertyFAQListSerializer, WebsiteFAQSerializer
from property.models import Property
from core.utils.response import PrepareResponse
from core.utils.pagination import CustomPageNumberPagination


# Hotel FAQ Views
class PropertyFAQCreateView(generics.GenericAPIView):
    serializer_class = PropertyFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        property_id = self.kwargs.get('property_id')
        try:
            property = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return PrepareResponse(success=False, message="Property not found").send(404)

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
    serializer_class = PropertyFAQListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        property_slug = self.kwargs.get('property_slug')

        return PropertyFAQ.objects.filter(property__slug=property_slug, parent__isnull=True).prefetch_related('replies')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        faq_count = queryset.count()

        # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response_data = paginated_response  
            paginated_response_data['faq_count'] = faq_count

            return PrepareResponse(
                success=True,
                message="Property FAQs retrieved successfully",
                data=paginated_response_data
            ).send(code=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Property FAQs retrieved successfully",
            data={
                'faq_count': faq_count,
                'results': serializer.data
            }
        ).send(code=status.HTTP_200_OK)

        


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
