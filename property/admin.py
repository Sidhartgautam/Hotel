from django.contrib import admin
from .models import PropertyCategory,Property,BreakfastInfo,ParkingInfo,PropertyImage,Amenity,PropertyAmenities,Policy
# Register your models here.
admin.site.register(PropertyCategory)
admin.site.register(Property)
admin.site.register(BreakfastInfo)
admin.site.register(ParkingInfo)
admin.site.register(PropertyImage)
admin.site.register(Amenity)
admin.site.register(PropertyAmenities)
admin.site.register(Policy)

class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ('property', 'cancellations_allowed', 'cancellation_fee_type', 'cancellation_fee_amount', 'refundable')
    search_fields = ('property__property_name',)
    list_filter = ('cancellations_allowed', 'refundable', 'cancellation_fee_type')

