from django.contrib import admin
from .models import WeeklyOffer
admin.site.register(WeeklyOffer)

# @admin.register(WeeklyOffer)
# class WeeklyOfferAdmin(admin.ModelAdmin):
#     list_display = ['property', 'discount_percentage', 'start_date', 'end_date', 'is_active']
#     list_filter = ['start_date', 'end_date', 'property']
#     search_fields = ['property__property_name', 'description']
