from django.contrib import admin
from .models import (
    Property,
    Amenity,
    BreakfastInfo,
    ParkingInfo,
    PropertyImage,
    PropertyAmenities,
    Policy,
    CancellationPolicy,
    SingleUnitPrice,
)

# Inlines with Stacked Layout for better spacing
class BreakfastInfoInline(admin.StackedInline):
    model = BreakfastInfo
    extra = 1
    fields = ('serve_breakfast', 'breakfast_included', 'breakfast_type', 'extra_cost')
    can_delete = True


class ParkingInfoInline(admin.StackedInline):
    model = ParkingInfo
    extra = 1
    fields = ('parking_availability', 'parking_price', 'reservation_required', 'parking_location', 'parking_access')
    can_delete = True


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 3
    fields = ('image',)
    can_delete = True


class PropertyAmenitiesInline(admin.StackedInline):
    model = PropertyAmenities
    extra = 1
    fields = ('amenity', 'is_available')
    can_delete = True


class PolicyInline(admin.StackedInline):
    model = Policy
    extra = 1
    fields = ('checkin_time', 'checkout_time', 'children_allowed', 'extra_beds_available', 'extra_bed_cost',
              'pets_allowed', 'pet_fee', 'pet_details')
    can_delete = True


class CancellationPolicyInline(admin.StackedInline):
    model = CancellationPolicy
    extra = 1
    fields = ('cancellations_allowed', 'cancellation_deadline_days', 'cancellation_fee_type',
              'cancellation_fee_amount', 'refundable', 'additional_notes')
    can_delete = True


class SingleUnitPriceInline(admin.StackedInline):
    model = SingleUnitPrice
    extra = 1
    fields = ('base_price_per_night', 'seasonal_price', 'discount_percentage')
    can_delete = False


# Property Admin
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'country', 'city', 'is_single_unit', 'star_rating_property')
    search_fields = ('property_name', 'address', 'city__name')
    list_filter = ('country', 'is_single_unit', 'star_rating_property')
    inlines = [
        BreakfastInfoInline,
        ParkingInfoInline,
        PropertyImageInline,
        PropertyAmenitiesInline,
        PolicyInline,
        CancellationPolicyInline,
        SingleUnitPriceInline,
    ]


# Register the Property model with its custom admin class
admin.site.register(Property, PropertyAdmin)
admin.site.register(Amenity)