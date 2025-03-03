from django.urls import path
from .views import (PropertySearchView,
                    TrendingDestinationsView,
                    PropertyListView,
                    PropertyCreateView,
                    PropertyCategoryListView,
                    PropertyByPropertyTypeView,
                    PropertyCancellationPolicyView,
                    PropertyDetailsView,
                    PolicyByPropertySlugView,
                    PropertyAmenitiesListView
)
urlpatterns = [
    path('properties/list/', PropertyListView.as_view(), name='property-list'),
    path('properties/create/', PropertyCreateView.as_view(), name='property-create'),
    path('search/', PropertySearchView.as_view(), name='property-search'),
    path('trending-destinations/lists/',TrendingDestinationsView.as_view(), name='tending-destiantion'),
    path('property-categories/lists/', PropertyCategoryListView.as_view(), name='property-category-list'),
    path('properties/by-type/<uuid:property_category_id>/', PropertyByPropertyTypeView.as_view(), name='property-by-property-type'),
    path('cancellation-policy/<uuid:property_id>/', PropertyCancellationPolicyView.as_view(), name='property-cancellation-policy'),
    path('properties/<str:slug>/details/',PropertyDetailsView.as_view(), name='property-details'),
    path('policies/<slug:slug>/', PolicyByPropertySlugView.as_view(), name='policy-by-property-slug'),
    path('properties/<str:property_slug>/amenities/', PropertyAmenitiesListView.as_view(), name='property-amenities-list'),
]