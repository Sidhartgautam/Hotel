from rest_framework import serializers
from .models import WeeklyOffer
import random

class WeeklyOfferSerializer(serializers.ModelSerializer):
    property_name=serializers.SerializerMethodField()
    slug=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model = WeeklyOffer
        fields = ['property_name', 'discount_percentage', 'start_date', 'end_date', 'description','image','slug']
    def get_property_name(self,obj):
        return obj.property.property_name
    def get_image(self, obj):
        images = obj.property.images.all() 
        if images.exists():
            return random.choice(images).image.url
        return None
    def get_slug(self,obj):
        return obj.property.slug
    
