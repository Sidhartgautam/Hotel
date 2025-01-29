from django.urls import path
from .views import (
    PropertyFAQCreateView, PropertyFAQListView, 
    WebsiteFAQCreateView, WebsiteFAQListView
)

urlpatterns = [
    # Hotel FAQs
    path('hotels/<uuid:hotel_id>/faqs/', PropertyFAQCreateView.as_view(), name='hotel-faq-list'),
    path('hotels/<uuid:hotel_id>/faqs/create/', PropertyFAQListView.as_view(), name='hotel-faq-create'),

    # Website FAQs
    path('website/faqs/', WebsiteFAQListView.as_view(), name='website-faq-list'),
    path('website/faqs/create/', WebsiteFAQCreateView.as_view(), name='website-faq-create'),
] 