# country/serializers.py
from rest_framework import serializers
from .models import Country, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'currency']

class CitySerializer(serializers.ModelSerializer):
    country_id = serializers.ReadOnlyField(source='country.id')
    country_name = serializers.ReadOnlyField(source='country.country_name')
    image=serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ['id', 'city_name', 'country_id', 'country_name', 'image']
    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        else:
            None

class PopularCitySerializer(serializers.ModelSerializer):
    hotel_count = serializers.SerializerMethodField()
    popular_count=serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'city_name', 'hotel_count', 'image', 'popular_count']

    def get_hotel_count(self, obj):
        return obj.hotels.count()

    def get_popular_count(self, obj):
        return obj.hotels.filter(city=obj).count()
    

