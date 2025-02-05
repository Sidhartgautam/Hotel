from django.urls import path
from .views import (
    PropertyFAQCreateView, PropertyFAQListView, 
    WebsiteFAQCreateView, WebsiteFAQListView
)

urlpatterns = [
    # Hotel FAQs
    path('property/<uuid:property_id>/create/', PropertyFAQCreateView.as_view(), name='hotel-faq-list'),
    path('property/<str:property_slug>/faqs/list/', PropertyFAQListView.as_view(), name='hotel-faq-create'),

    # Website FAQs
    path('website/faqs/lists/', WebsiteFAQListView.as_view(), name='website-faq-list'),
    path('website/faqs/create/', WebsiteFAQCreateView.as_view(), name='website-faq-create'),
] 