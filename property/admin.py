# from django.contrib import admin
# from .models import (
#     Property,
#     PropertyCategory,
#     Amenity,
#     BreakfastInfo,
#     ParkingInfo,
#     PropertyImage,
#     PropertyAmenities,
#     Policy,
#     CancellationPolicy,
#     SingleUnitPrice,
# )

# # Inlines with Stacked Layout for better spacing
# class BreakfastInfoInline(admin.StackedInline):
#     model = BreakfastInfo
#     extra = 1
#     fields = ('serve_breakfast', 'breakfast_included', 'breakfast_type', 'extra_cost')
#     can_delete = True


# class ParkingInfoInline(admin.StackedInline):
#     model = ParkingInfo
#     extra = 1
#     fields = ('parking_availability', 'parking_price', 'reservation_required', 'parking_location', 'parking_access')
#     can_delete = True


# class PropertyImageInline(admin.StackedInline):
#     model = PropertyImage
#     extra = 3
#     fields = ('image',)
#     can_delete = True


# class PropertyAmenitiesInline(admin.StackedInline):
#     model = PropertyAmenities
#     extra = 1
#     fields = ('amenity', 'is_available')
#     can_delete = True


# class PolicyInline(admin.StackedInline):
#     model = Policy
#     extra = 1
#     fields = ('checkin_time_from', 'checkin_time_to', 'checkout_time_from', 'checkout_time_to', 'children_allowed', 'extra_beds_available', 'extra_bed_cost',
#               'pets_allowed', 'pet_fee', 'pet_details')
#     can_delete = True


# class CancellationPolicyInline(admin.StackedInline):
#     model = CancellationPolicy
#     extra = 1
#     fields = ('cancellations_allowed', 'cancellation_deadline_days', 'cancellation_fee_type',
#               'cancellation_fee_amount', 'refundable', 'additional_notes')
#     can_delete = True


# class SingleUnitPriceInline(admin.StackedInline):
#     model = SingleUnitPrice
#     extra = 1
#     fields = ('base_price_per_night', 'seasonal_price', 'discount_percentage')
#     can_delete = False


# # Property Admin
# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ('property_name', 'country', 'city', 'is_single_unit', 'star_rating_property')
#     search_fields = ('property_name', 'address', 'city__name')
#     list_filter = ('country', 'is_single_unit', 'star_rating_property')
#     inlines = [
#         BreakfastInfoInline,
#         ParkingInfoInline,
#         PropertyImageInline,
#         PropertyAmenitiesInline,
#         PolicyInline,
#         CancellationPolicyInline,
#         SingleUnitPriceInline,
#     ]


# # Register the Property model with its custom admin class
# admin.site.register(Property, PropertyAdmin)
# admin.site.register(Amenity)
# admin.site.register(PropertyCategory)

from django.contrib import admin
from django.db import models
from .models import (
    Property,
    PropertyCategory,
    Amenity,
    BreakfastInfo,
    ParkingInfo,
    PropertyImage,
    PropertyAmenities,
    Policy,
    CancellationPolicy,
    SingleUnitPrice,
)


### Optimized Inlines with Limited Querysets ###

class BreakfastInfoInline(admin.StackedInline):
    model = BreakfastInfo
    extra = 0  # No extra blank forms
    fields = ('serve_breakfast', 'breakfast_included', 'breakfast_type', 'extra_cost')
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:1]  # Load only 1 breakfast info to optimize


class ParkingInfoInline(admin.StackedInline):
    model = ParkingInfo
    extra = 0
    fields = ('parking_availability', 'parking_price', 'reservation_required', 'parking_location', 'parking_access')
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:1]  # Load only 1 parking info


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0
    fields = ('image',)
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:3]  # Load only 3 images per property


class PropertyAmenitiesInline(admin.StackedInline):
    model = PropertyAmenities
    extra = 0
    fields = ('amenity', 'is_available')
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:5]  # Load only 5 amenities


class PolicyInline(admin.StackedInline):
    model = Policy
    extra = 0
    fields = ('checkin_time_from', 'checkin_time_to', 'checkout_time_from', 'checkout_time_to', 'children_allowed', 
              'extra_beds_available', 'extra_bed_cost', 'pets_allowed', 'pet_fee', 'pet_details')
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:1]  # Load only 1 policy record


class CancellationPolicyInline(admin.StackedInline):
    model = CancellationPolicy
    extra = 0
    fields = ('cancellations_allowed', 'cancellation_deadline_days', 'cancellation_fee_type',
              'cancellation_fee_amount', 'refundable', 'additional_notes')
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:1]  # Load only 1 cancellation policy


class SingleUnitPriceInline(admin.StackedInline):
    model = SingleUnitPrice
    extra = 0
    fields = ('base_price_per_night', 'seasonal_price', 'discount_percentage')
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:1]  # Load only 1 price info


### Optimized Property Admin ###
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'country', 'city', 'is_single_unit', 'star_rating_property')
    search_fields = ('property_name', 'address', 'city__name')
    list_filter = ('country', 'is_single_unit', 'star_rating_property')

    # Use raw_id_fields for ForeignKeys to speed up admin
    raw_id_fields = ('city',)
    autocomplete_fields = ['country']

    # Optimized QuerySet to reduce database load
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('country', 'city').prefetch_related('propertyimage_set')

    # Add optimized inlines
    inlines = [
        BreakfastInfoInline,
        ParkingInfoInline,
        PropertyImageInline,
        PropertyAmenitiesInline,
        PolicyInline,
        CancellationPolicyInline,
        SingleUnitPriceInline,
    ]


### Optimized Amenity Admin ###
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request)[:20]  # Load only 20 amenities


### Optimized PropertyCategory Admin ###
@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

    def get_queryset(self, request):
        return super().get_queryset(request)[:10]  # Load only 10 property categories
