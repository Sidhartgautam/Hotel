from django.contrib import admin
from django.db import models
from .models import RoomType, RoomAmenities, RoomBed, Price, RoomImages, RoomAvailability

class RoomAvailabilityInline(admin.TabularInline):
    model = RoomAvailability
    extra = 5  # Allow adding up to 5 future availability entries
    fields = ['date', 'available_rooms']
    ordering = ['date']  # Show availability in ascending order
    can_delete = True


### ✅ Room Amenities Inline ###
class RoomAmenitiesInline(admin.StackedInline):
    model = RoomAmenities
    extra = 0
    can_delete = False  
    verbose_name = "Room Amenity"
    verbose_name_plural = "Room Amenities"


### ✅ Room Bed Inline ###
class RoomBedInline(admin.TabularInline):
    model = RoomBed
    extra = 1
    fields = ['bed_type', 'quantity']
    can_delete = True


### ✅ Price Inline ###
class PriceInline(admin.StackedInline):
    model = Price
    extra = 0
    fields = ['base_price_per_night', 'extra_guest_price', 'breakfast_price', 'parking_price',
              'is_seasonal', 'start_date', 'end_date', 'discount_percentage', 'currency']
    can_delete = True


### ✅ Room Images Inline ###
class RoomImagesInline(admin.TabularInline):
    model = RoomImages
    extra = 2
    fields = ['image']
    can_delete = True


### ✅ Updated RoomType Admin with RoomAvailability Inline ###
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('property', 'room_type', 'room_name', 'max_no_of_guests', 'room_size', 'smoking_allowed')
    search_fields = ('property__property_name', 'room_name')
    list_filter = ('room_type', 'smoking_allowed', 'property')
    ordering = ['property', 'room_type']

    # ✅ Optimized Query to Prefetch Related Data (Boosts Admin Performance)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('property').prefetch_related(
            'room_amenities', 'room_beds', 'prices', 'availabilities'
        )

    fieldsets = [
        ('General Information', {
            'fields': (
                'property', 'room_type', 'room_name',
                'max_no_of_guests', 'room_size', 'smoking_allowed'
            ),
        }),
    ]

    inlines = [RoomAmenitiesInline, RoomBedInline, PriceInline, RoomImagesInline, RoomAvailabilityInline]
