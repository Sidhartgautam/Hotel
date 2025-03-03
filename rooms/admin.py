# from django.contrib import admin
# from .models import (
#     BedType,
#     RoomAmenities,
#     RoomType,
#     RoomBed,
#     Price,
#     RoomImages,
# )
# from django.db import models

# # Inline classes for related models

# # class RoomAmenitiesInline(admin.StackedInline):
# #     model = RoomAmenities
# #     extra = 0  # No extra blank forms
# #     fields = [
# #         'air_conditioning', 'free_wifi', 'television', 'minibar', 'wardrobe', 'desk',
# #         'telephone', 'safe', 'soundproofing', 'ironing_facilities', 'extra_long_beds',
# #         'electric_blankets', 'garden_view', 'city_view', 'mountain_view', 'landmark_view',
# #         'pool_view', 'attached_bathroom', 'free_toiletries', 'shower', 'bathtub',
# #         'balcony', 'patio', 'terrace', 'private_entrance', 'kitchenette', 'heating'
# #     ]
# #     can_delete = False  
# #     verbose_name = "Room Amenity"
# #     verbose_name_plural = "Room Amenities"
# class RoomAmenitiesInline(admin.StackedInline):
#     model = RoomAmenities
#     extra = 0  # No extra blank forms
#     can_delete = False  
#     verbose_name = "Room Amenity"
#     verbose_name_plural = "Room Amenities"

#     # Automatically fetch all boolean fields from RoomAmenities
#     def get_fields(self, request, obj=None):
#         boolean_fields = [field.name for field in RoomAmenities._meta.get_fields() if isinstance(field, models.BooleanField)]
#         return boolean_fields

#     # Override the default field list
#     def formfield_for_dbfield(self, db_field, request, **kwargs):
#         if isinstance(db_field, models.BooleanField):
#             kwargs["required"] = False  # Ensure optional selection
#         return super().formfield_for_dbfield(db_field, request, **kwargs)



# class RoomBedInline(admin.TabularInline):
#     model = RoomBed
#     extra = 1
#     fields = ['bed_type', 'quantity']
#     can_delete = True


# class PriceInline(admin.StackedInline):
#     model = Price
#     extra = 0
#     fields = [
#         'base_price_per_night', 'extra_guest_price', 'breakfast_price', 'parking_price',
#         'is_seasonal', 'start_date', 'end_date', 'discount_percentage', 'currency'
#     ]
#     can_delete = True
#     verbose_name = "Price"
#     verbose_name_plural = "Prices"


# class RoomImagesInline(admin.TabularInline):
#     model = RoomImages
#     extra = 2
#     fields = ['image']
#     can_delete = True


# # RoomType Admin with inlines
# @admin.register(RoomType)
# class RoomTypeAdmin(admin.ModelAdmin):
#     list_display = (
#         'property', 'room_type', 'room_name', 'no_of_available_rooms',
#         'max_no_of_guests', 'room_size', 'smoking_allowed'
#     )
#     search_fields = ('property__property_name', 'room_name', 'room_type')
#     list_filter = ('room_type', 'smoking_allowed', 'property')
#     inlines = [RoomAmenitiesInline, RoomBedInline, PriceInline, RoomImagesInline]

#     fieldsets = [
#         ('General Information', {
#             'fields': (
#                 'property', 'room_type', 'room_name', 'no_of_available_rooms',
#                 'max_no_of_guests', 'room_size', 'smoking_allowed'
#             ),
#         }),
#     ]


# # Admin class for BedType
# @admin.register(BedType)
# class BedTypeAdmin(admin.ModelAdmin):
#     list_display = ('bed_type',)
#     search_fields = ('bed_type',)


# # Admin class for RoomAmenities (if you need to view them separately)
# @admin.register(RoomAmenities)
# class RoomAmenitiesAdmin(admin.ModelAdmin):
#     list_display = (
#      'room_type', 'air_conditioning', 'free_wifi', 'television', 'balcony', 'attached_bathroom'
#     )
#     search_fields = ('room_type__room_name',)
#     list_filter = (
#         'air_conditioning', 'free_wifi', 'television', 'balcony', 'attached_bathroom'
#     )


# # Admin class for Price
# @admin.register(Price)
# class PriceAdmin(admin.ModelAdmin):
#     list_display = (
#         'property', 'room_type', 'base_price_per_night', 'currency',
#         'is_seasonal', 'discount_percentage'
#     )
#     list_filter = ('is_seasonal', 'currency')
#     search_fields = ('property__property_name', 'room_type__room_name')


# # Admin class for RoomImages
# @admin.register(RoomImages)
# class RoomImagesAdmin(admin.ModelAdmin):
#     list_display = ('room_type', 'image')
#     search_fields = ('room_type__room_name',)

from django.contrib import admin
from django.db import models
from .models import RoomType, RoomAmenities, RoomBed, Price, RoomImages


### ✅ Optimized Inlines ###
class RoomAmenitiesInline(admin.StackedInline):
    model = RoomAmenities
    extra = 0
    can_delete = False  
    verbose_name = "Room Amenity"
    verbose_name_plural = "Room Amenities"

    def get_queryset(self, request):
        return super().get_queryset(request)  # Limit to 5 amenities


class RoomBedInline(admin.TabularInline):
    model = RoomBed
    extra = 1
    fields = ['bed_type', 'quantity']
    can_delete = True

    def get_queryset(self, request):
        return super().get_queryset(request)  


class PriceInline(admin.StackedInline):
    model = Price
    extra = 0
    fields = ['base_price_per_night', 'extra_guest_price', 'breakfast_price', 'parking_price',
              'is_seasonal', 'start_date', 'end_date', 'discount_percentage', 'currency']
    can_delete = True

    def get_queryset(self, request):
        return super().get_queryset(request)  


class RoomImagesInline(admin.TabularInline):
    model = RoomImages
    extra = 2
    fields = ['image']
    can_delete = True

    def get_queryset(self, request):
        return super().get_queryset(request)  


### ✅ Fixed RoomType Admin ###
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('property', 'room_type', 'room_name', 'no_of_available_rooms', 'max_no_of_guests', 'room_size', 'smoking_allowed')

    # ✅ Fix: Ensure `search_fields` is properly set
    search_fields = ('property__property_name', 'room_name')

    list_filter = ('room_type', 'smoking_allowed', 'property')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('property').prefetch_related('room_amenities', 'room_beds', 'prices')

    inlines = [RoomAmenitiesInline, RoomBedInline, PriceInline, RoomImagesInline]  
