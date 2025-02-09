from django.urls import path
from .views import (PropertyCreateView,
                    ParkingInfoCreateView,
                    BreakfastInfoCreateView,
                    PropertyAmenitiesCreateView,
                    PropertyImageCreateView,
                    PolicyCreateView,
                    PropertyUpdateDeleteView,
                    ParkingInfoUpdateDeleteView,
                    BreakfastInfoUpdateDeleteView,
                    PolicyUpdateDeleteView,
                    PropertyAmenitiesUpdateDeleteView,
                    PropertyImageUpdateDeleteView,
                    RoomImagesBulkCreateView,
                    RoomAmenitiesCreateView,
                    RoomTypeCreateView,
                    RoomBedCreateView,
                    PriceCreateView,
                    RoomAmenitiesUpdateDeleteView,
                    RoomTypeUpdateDeleteView,
                    RoomImagesUpdateDeleteView,
                    RoomBedUpdateDeleteView,
                    PriceUpdateDeleteView,
                    CancellationPolicyCreateView,
                    CancellationPolicyUpdateDeleteView,
                    PropertyFAQCreateView,
                    WeeklyOfferCreateView,
                    WeeklyOfferListView,
                    SinglePropertyPriceCreateView

                    



)

urlpatterns = [
    #########################PropertyCreate#########################################
    path('properties/create/', PropertyCreateView.as_view(), name='property-create'),
    path('parkinginfo/create/', ParkingInfoCreateView.as_view(), name='parkinginfo-create'),
    path('breakfastinfo/create/', BreakfastInfoCreateView.as_view(), name='breakfastinfo-create'),
    path('property-amenities/create/',PropertyAmenitiesCreateView.as_view(),name='amenities-create'),
    path('propertyimages/create/', PropertyImageCreateView.as_view(), name='propertyimages-create'),
    path('policies/create/', PolicyCreateView.as_view(), name='policies-create'),
    path('cancellation-policy/create/', CancellationPolicyCreateView.as_view(), name='cancellation-policy-create'),
    path('single-property-price/create/', SinglePropertyPriceCreateView.as_view(), name='single-property-price-create'),
    

    ##############################PropertyUpdate#########################################
    path('properties/<uuid:pk>/', PropertyUpdateDeleteView.as_view(), name='property-update-delete'),
    path('parkinginfo/<uuid:pk>/', ParkingInfoUpdateDeleteView.as_view(), name='parkinginfo-update-delete'),
    path('breakfastinfo/<uuid:pk>/', BreakfastInfoUpdateDeleteView.as_view(), name='breakfastinfo-update-delete'),
    path('policies/<uuid:pk>/', PolicyUpdateDeleteView.as_view(), name='policy-update-delete'),
    path('property-amenities/<uuid:pk>/', PropertyAmenitiesUpdateDeleteView.as_view(), name='property-amenities-update-delete'),
    path('property-images/<uuid:pk>/', PropertyImageUpdateDeleteView.as_view(), name='property-image-update-delete'),
    path('cancellation-policy/<uuid:pk>/', CancellationPolicyUpdateDeleteView.as_view(), name='cancellation-policy-update-delete'),

    ###############################Room_type create########################################
    path('room-images/bulk-create/', RoomImagesBulkCreateView.as_view(), name='room-images-bulk-create'),
    path('room-amenities/create/', RoomAmenitiesCreateView.as_view(), name='room-amenities-create'),
    path('room-types/create/', RoomTypeCreateView.as_view(), name='room-type-create'),
    path('room-beds/create/', RoomBedCreateView.as_view(), name='room-bed-create'),
    path('prices/create/', PriceCreateView.as_view(), name='price-create'),

    ############################Room_type_update###################################
    path('room-amenities/<uuid:pk>/', RoomAmenitiesUpdateDeleteView.as_view(), name='room-amenities-update-delete'),
    path('room-types/<uuid:pk>/', RoomTypeUpdateDeleteView.as_view(), name='room-type-update-delete'),
    path('room-images/<uuid:pk>/', RoomImagesUpdateDeleteView.as_view(), name='room-images-update-delete'),
    path('room-beds/<uuid:pk>/', RoomBedUpdateDeleteView.as_view(), name='room-bed-update-delete'),
    path('prices/<uuid:pk>/', PriceUpdateDeleteView.as_view(), name='price-update-delete'),

    #################################PropertyFAQCreate#########################################
    path('property/<slug:property_slug>/faq/create/', PropertyFAQCreateView.as_view(), name='property-faq-create'),

    #################################WeeklyOfferCreate#########################################
    path('weekly-offer/create/', WeeklyOfferCreateView.as_view(), name='weekly-offer-create'),
    path('weekly-offer/list/', WeeklyOfferListView.as_view(), name='weekly-offer-list'),
]
