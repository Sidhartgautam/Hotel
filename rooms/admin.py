from django.contrib import admin
from .models import (
    BedType,
    RoomAmenities,
    RoomType,
    RoomBed,
    Price,
    RoomImages,
)

# Inline classes for related models

class RoomAmenitiesInline(admin.StackedInline):
    model = RoomAmenities
    extra = 0
    fields = [
        'air_conditioning', 'free_wifi', 'television', 'minibar', 'wardrobe', 'desk',
        'telephone', 'safe', 'soundproofing', 'ironing_facilities', 'extra_long_beds',
        'electric_blankets', 'garden_view', 'city_view', 'mountain_view', 'landmark_view',
        'pool_view', 'attached_bathroom', 'free_toiletries', 'shower', 'bathtub',
        'balcony', 'patio', 'terrace', 'private_entrance', 'kitchenette', 'heating'
    ]
    can_delete = True
    verbose_name = "Room Amenity"
    verbose_name_plural = "Room Amenities"


class RoomBedInline(admin.TabularInline):
    model = RoomBed
    extra = 1
    fields = ['bed_type', 'quantity']
    can_delete = True


class PriceInline(admin.StackedInline):
    model = Price
    extra = 0
    fields = [
        'base_price_per_night', 'extra_guest_price', 'breakfast_price', 'parking_price',
        'is_seasonal', 'start_date', 'end_date', 'discount_percentage', 'currency'
    ]
    can_delete = True
    verbose_name = "Price"
    verbose_name_plural = "Prices"


class RoomImagesInline(admin.TabularInline):
    model = RoomImages
    extra = 2
    fields = ['image']
    can_delete = True


# RoomType Admin with inlines
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = (
        'property', 'room_type', 'room_name', 'no_of_available_rooms',
        'max_no_of_guests', 'room_size', 'smoking_allowed'
    )
    search_fields = ('property__property_name', 'room_name', 'room_type')
    list_filter = ('room_type', 'smoking_allowed', 'property')
    inlines = [RoomAmenitiesInline, RoomBedInline, PriceInline, RoomImagesInline]

    fieldsets = [
        ('General Information', {
            'fields': (
                'property', 'room_type', 'room_name', 'no_of_available_rooms',
                'max_no_of_guests', 'room_size', 'smoking_allowed'
            ),
        }),
    ]


# Admin class for BedType
@admin.register(BedType)
class BedTypeAdmin(admin.ModelAdmin):
    list_display = ('bed_type',)
    search_fields = ('bed_type',)


# Admin class for RoomAmenities (if you need to view them separately)
@admin.register(RoomAmenities)
class RoomAmenitiesAdmin(admin.ModelAdmin):
    list_display = (
        'room_type', 'air_conditioning', 'free_wifi', 'television', 'balcony', 'attached_bathroom'
    )
    search_fields = ('room_type__room_name',)
    list_filter = (
        'air_conditioning', 'free_wifi', 'television', 'balcony', 'attached_bathroom'
    )


# Admin class for Price
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'property', 'room_type', 'base_price_per_night', 'currency',
        'is_seasonal', 'discount_percentage'
    )
    list_filter = ('is_seasonal', 'currency')
    search_fields = ('property__property_name', 'room_type__room_name')


# Admin class for RoomImages
@admin.register(RoomImages)
class RoomImagesAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'image')
    search_fields = ('room_type__room_name',)
