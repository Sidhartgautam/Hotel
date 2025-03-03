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
    

class AllOfferSerializer(serializers.ModelSerializer):
    property_name=serializers.SerializerMethodField()
    slug=serializers.SerializerMethodField()
    banner=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    class Meta:
        model = WeeklyOffer
        fields = ['property_name','title', 'description','banner','slug']
    def get_property_name(self,obj):
        return obj.property.property_name
    def get_banner(self, obj):
        images = obj.property.images.all() 
        if images.exists():
            return random.choice(images).image.url
        return None
    def get_slug(self,obj):
        return obj.property.slug
    
    def get_title(self,obj):
        return f"Get {obj.discount_percentage}% OFF on your stay at {obj.property.property_name}"
    
