from django.contrib import admin
from .models import BedType,RoomAmenities,RoomType,RoomBed,Price,RoomImages
# Register your models here.
admin.site.register(BedType)
admin.site.register(RoomAmenities)
admin.site.register(RoomType)
admin.site.register(RoomBed)
admin.site.register(Price)
admin.site.register(RoomImages)
